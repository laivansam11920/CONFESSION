from app.services.update_cfs.update_uncertain import UpdateUncertain

from flask import request

class ModerationUncertainCfs:

    def check(self, key_success: bool, cfs_id: str | None = None):

        if not key_success or not cfs_id:
            return

        safe = request.form.get('safe_to_post') == "True"

        if not UpdateUncertain.update_uncertain(cfs_id=cfs_id, safe_to_post=safe):
            ...

        #TODO: sự dụng các methods như delete để thay thế

