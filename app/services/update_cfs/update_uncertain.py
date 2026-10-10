from app.services.moderation.scan_pending_confessions import ModerationQueueScanner
from app.utils.logger import console


class UpdateUncertain:

    @staticmethod
    def update_uncertain(cfs_id: str | None, safe_to_post: bool) -> bool:
        try:

            if not cfs_id:
                return False

            if safe_to_post:
                return ModerationQueueScanner.approve_by_human(cfs_id)

            return ModerationQueueScanner.reject_by_human(cfs_id)

        except Exception as e:
            console.error(e)
            return False
