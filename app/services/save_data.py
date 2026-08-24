from app.schema.confession import ConfessionSchema
from app.utils.logger import logger
from app.utils.check_similar import is_similar
from base import ConfessionManager
from configs import Config

from dataclasses import asdict
from time import time

from flask_babel import Babel, gettext as _

__all__ = ["SaveConfession"]


class SaveData(ConfessionManager):

    def save_to_db(self, confession_data: ConfessionSchema) -> dict:
        try:

            if Config.CHECK_SAME_DOCS:

                old_docs = (
                    self.db.docs.find(
                        {
                            "post_time": {
                                "$gte": int(time()) - Config.TIME_OUT_CONFESSION
                            },
                            "send": False,
                        },
                        {"_id": 1, "confession_id": 1, "confession": 1, "send": 1},
                    )
                    .sort("_id", -1)
                    .limit(100)
                )

                matched_id = None

                for doc in old_docs:
                    if is_similar(
                        confession_data.confession, doc.get("confession", "")
                    ):
                        matched_id = doc["confession_id"]
                        break

                if matched_id is not None:
                    self.db.docs.update_one(
                        {"confession_id": matched_id}, {"$inc": {"same_post_count": 1}}
                    )
                    return {
                        "success": True,
                        "msg": _(
                            "Nội dung này có vẻ trùng với bài trước, hệ thống đã tự động cộng dồn lượt tương tự cho bạn rồi nhé!"
                        ),
                        "status": "success",
                    }

            cfs_docs = self.db.cfs_count.find_one_and_update(
                {"id": "confession_id"},
                {"$inc": {"seq": 1}},
                upsert=True,
            )

            confession_data_dict = asdict(confession_data)
            confession_data_dict["cfs"] = int(
                (cfs_docs or {}).get("seq", 0)
            )  # NÊN KIỂM DUYỆT BẰNG AI TRƯỚC KHI GẮN CFS NUMS
            self.db.docs.insert_one(confession_data_dict)
            return {
                "success": True,
                "msg": _("Lưu confession thành công rồi nhé!"),
                "status": "success",
            }

        except Exception as e:
            logger.error(e)
            return {
                "success": False,
                "msg": _(
                    "Rất tiếc, có chút sự cố nhỏ khi lưu confession. Bạn thử lại giúp chúng mình nha."
                ),
                "status": "error",
            }


SaveConfession: SaveData = SaveData()


# TODO: PHẢI LÀM SAO NẾU MỘT NGƯỜI SPAM NHIỀU CONFESSION NHƯNG KHÔNG THỂ XÁC NHẬN DANH TÍNH, CẦN SỰ DỤNG AI HOẶC CÁC CÔNG CỤ MẠNH, HOẶC NHỜ ĐẾN SỰ KIỂM DUYỆT CỦA CON NGƯỜI.
