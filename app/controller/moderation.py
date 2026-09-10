from app.services.moderation.check_key import CheckKeyModerationService


@CheckKeyModerationService.check
def moderation_ctl(cfs_id: str | None = None):
    from flask import render_template
    from app.services.get_data.get_uncertain_cfs import GetData

    data = GetData.get(cfs_id)

    return render_template(
        "moderation/action.html",
        confession=data.confession,
        post_time=data.post_time,
        score=data.ai_data.get("score", "?"),
        reason=data.ai_data.get("reason", "?"),
    )


@CheckKeyModerationService.check
def moderation_api_ctl(cfs_id: str | None = None):
    from flask import flash, redirect, url_for, request
    from app.services.update_cfs.update_uncertain import UpdateUncertain
    from flask_babel import gettext as _

    msg = ""
    _accept = False
    action = request.form.get("action", "?")

    if action == "accept":
        _accept = True
        msg = _("Thành công chấp thuận confession")

    UpdateUncertain.update_uncertain(cfs_id, _accept)
    flash(msg or _("Đã xóa thành công confession"))
    return redirect(url_for("moderation.moderation_route"))
