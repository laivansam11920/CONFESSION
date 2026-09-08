from flask import request, redirect, url_for, Response, render_template
from flask_babel import _


def home() -> Response:
    return redirect(
        url_for(
            "main_route.index",
            lang=request.args.get(
                "lang", request.accept_languages.best_match(["vi", "en"])
            ),
        )
    )


def home_moderation() -> str:

    text: str = _("Không được hiện thị")

    return render_template(
        "moderation/action.html",
        confession=text,
        post_time=text,
        score=text,
        reason=text,
    )
