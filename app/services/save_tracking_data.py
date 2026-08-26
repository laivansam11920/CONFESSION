def save_tracking_id(db, **kwargs):
    db.docs.update_one(
        {"confession_id": kwargs["confession_id"]},
        {
            "$addToSet": {
                "user_tracking_data.ip": kwargs["data"]["ip"],
                "user_tracking_data.fingerprint": kwargs["data"]["fingerprint"],
            }
        },
    )
