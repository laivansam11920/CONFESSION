from app.schema.confession import ConfessionSchema
from app.schema.ReturnSchema import ReturnSchema
from app.utils.logger import console
from app.utils.check_similar import is_similar
from app.utils.get_cfs_count import cfs_nums
from app.database import db
from app.services.moderation.update_cfs_moderation import ConfessionModeration
from app.services.tracking_user.get_user_tracking import TrackingService
from configs import Config

from dataclasses import asdict
from time import time

from flask_babel import gettext as _

__all__ = ["SaveConfession"]


class SaveConfession:

    @staticmethod
    @TrackingService.save_user_tracking
    @ConfessionModeration.update_cfs_moderation
    def save_cfs(confession_data: ConfessionSchema) -> ReturnSchema:
        try:

            if Config.CHECK_SAME_DOCS:

                old_docs = (
                    db.docs.find(
                        {
                            "post_time": {
                                "$gte": int(time()) - Config.TIME_OUT_CONFESSION
                            },
                            "send": False,
                        },
                        {"_id": 1, "confession_id": 1, "confession": 1},
                    )
                    .sort("_id", -1)
                    .limit(Config.MAX_DOCS_GET)
                )

                matched_id = None

                for doc in old_docs:
                    if is_similar(
                        confession_data.confession, doc.get("confession", "")
                    ):
                        matched_id = doc["confession_id"]
                        break

                if matched_id is not None:
                    db.docs.update_one(
                        {"confession_id": matched_id}, {"$inc": {"same_post_count": 1}}
                    )

                    return ReturnSchema(
                        success=True,
                        msg=_(
                            "Nội dung này có vẻ trùng với bài trước, hệ thống đã tự động cộng dồn lượt tương tự cho bạn rồi nhé!"
                        ),
                        status="success",
                        data={
                            "confession_id": matched_id,
                        },
                    )

            confession_data_dict = asdict(confession_data)

            if not Config.MODERATION_CONFESSION:
                confession_data_dict["cfs"] = cfs_nums()

            db.docs.insert_one(confession_data_dict)

            return ReturnSchema(
                success=True,
                msg=_("Lưu confession thành công rồi nhé!"),
                status="success",
                data={
                    "confession_id": confession_data_dict["confession_id"],
                },
            )

        except Exception as e:
            console.error(e)
            return ReturnSchema()


# TODO: PHẢI LÀM SAO NẾU MỘT NGƯỜI SPAM NHIỀU CONFESSION NHƯNG KHÔNG THỂ XÁC NHẬN DANH TÍNH, CẦN SỰ DỤNG AI HOẶC CÁC CÔNG CỤ MẠNH, HOẶC NHỜ ĐẾN SỰ KIỂM DUYỆT CỦA CON NGƯỜI.
