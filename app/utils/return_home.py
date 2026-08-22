from flask import request, redirect, url_for, Response


def home() -> Response:
    return redirect(
        url_for(
            "main_route.index",
            lang=request.args.get(
                "lang", request.accept_languages.best_match(["vi", "en"])
            ),
        )
    )
