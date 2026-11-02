from app.database import db
from app.utils.get_cfs_count import cfs_nums
from app.utils.logger import console
from configs import Config

__all__ = ["ModerationQueueScanner"]


class ModerationQueueScanner:

    @staticmethod
    def _approve(confession_id: str, status: str) -> bool:
        if not confession_id:
            return False

        docs = (
            db.docs.find_one(
                {"confession_id": confession_id, "send": False},
                {"_id": 0, "cfs": 1, "safe_to_post": 1},
            )
            or {}
        )

        if not docs:
            return False

        update_data = {"safe_to_post": True, "status": status}

        if not docs.get("cfs"):
            update_data["cfs"] = cfs_nums()

        db.docs.update_one(
            {"confession_id": confession_id, "send": False},
            {"$set": update_data},
        )
        return True

    @staticmethod
    def _mark_manual_review(confession_id: str) -> bool:
        if not confession_id:
            return False

        db.docs.update_one(
            {"confession_id": confession_id, "send": False, "safe_to_post": False},
            {"$set": {"status": "need_human_review"}},
        )
        return True

    @staticmethod
    def _mark_blocked(confession_id: str) -> bool:
        if not confession_id:
            return False

        db.docs.update_one(
            {"confession_id": confession_id, "send": False},
            {
                "$set": {
                    "safe_to_post": False,
                    "status": "blocked_by_auto_scan",
                    "humans_check_safe": False,
                }
            },
        )
        return True

    @classmethod
    def approve_by_human(cls, confession_id: str) -> bool:
        return cls._approve(confession_id, "approved_by_human")

    @staticmethod
    def reject_by_human(confession_id: str) -> bool:
        if not confession_id:
            return False

        db.docs.update_one(
            {"confession_id": confession_id, "send": False},
            {
                "$set": {
                    "safe_to_post": False,
                    "status": "rejected_by_human",
                    "humans_check_safe": False,
                }
            },
        )
        return True

    @classmethod
    def scan(cls, confession_id: str | None = None) -> dict[str, int]:
        stats = {
            "approved": 0,
            "need_human_review": 0,
            "blocked": 0,
            "errors": 0,
        }

        query: dict = {"send": False}
        if confession_id:
            query["confession_id"] = confession_id

        docs = db.docs.find(
            query,
            {
                "_id": 0,
                "confession_id": 1,
                "ai_data": 1,
                "humans_check_safe": 1,
                "safe_to_post": 1,
            },
        )

        for doc in docs:
            try:
                cfs_id = doc.get("confession_id", "")
                if not cfs_id:
                    stats["errors"] += 1
                    continue

                if doc.get("humans_check_safe", False):
                    if cls.approve_by_human(cfs_id):
                        stats["approved"] += 1
                    continue

                ai_data = doc.get("ai_data", {}) or {}
                uncertain = ai_data.get("uncertain", True)
                score = ai_data.get("score")

                if not Config.MODERATION_CONFESSION:
                    if cls._mark_manual_review(cfs_id):
                        stats["need_human_review"] += 1
                    continue

                if uncertain or score is None:
                    if cls._mark_manual_review(cfs_id):
                        stats["need_human_review"] += 1
                    continue

                if score > Config.MAX_MODERATION_SCORE:
                    if cls._approve(cfs_id, "approved_by_auto_scan"):
                        stats["approved"] += 1
                    continue

                if cls._mark_blocked(cfs_id):
                    stats["blocked"] += 1
            except Exception as e:
                console.error(e)
                stats["errors"] += 1

        return stats

