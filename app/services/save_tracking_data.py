def save_tracking_id(db, **kwargs):
    db.docs.update_one(
        {"confession_id": kwargs["confession_id"]},
        {
            "$set": {
                "user_tracking_data": kwargs["data"],
            }
        },
    )

# lưu ip và fingerpint dưới dạng dict để có thể lưu đưcọ nhiều ip hơn(trường hợp phát hiện trùng bản gi)