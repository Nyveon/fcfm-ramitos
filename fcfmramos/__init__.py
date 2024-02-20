from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy

from fcfmramos import config
from fcfmramos.views import auth, main


def create_app():
    app = Flask(__name__)
    app.secret_key = config.secret_key

    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
        SQLALCHEMY_DATABASE_URI="sqlite:///project.db",
    )

    db = SQLAlchemy(app)

    @app.before_first_request
    def create_tables():
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

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    return app
