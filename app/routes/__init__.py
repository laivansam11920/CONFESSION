from flask import Flask, Blueprint

from .home import home_bp

__all__ = ["register_blueprints"]


def register_blueprints(app: Flask) -> None:
    try:

        blueprints: tuple[Blueprint] = (home_bp,)

        for bp in blueprints:
            app.register_blueprint(bp)

    except Exception as e:
        raise RuntimeError(f"Error while registering blueprints: {e}") from e
