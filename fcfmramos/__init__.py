from flask import Flask
from flask import session

from fcfmramos import config


def create_app():
    app = Flask(__name__)
    app.secret_key = config.secret_key

    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
        SQLALCHEMY_DATABASE_URI="sqlite:///project.sqlite",
    )

    from fcfmramos.model import db
    db.init_app(app)

    @app.cli.command()
    def createdb():
        db.create_all()

    @app.context_processor
    def inject_logged_in():
        return dict(is_logged_in=auth.is_logged_in())

    @app.context_processor
    def inject_username():
        return dict(username=session.get("username", ""))

    @app.context_processor
    def inject_verified():
        return dict(is_verified=auth.is_verified())

    from fcfmramos.view import auth, main
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    return app
