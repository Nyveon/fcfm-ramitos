from flask import Flask
from flask import session

from fcfmramos import config
from fcfmramos.views import auth, main

# cred = credentials.Certificate("fbconfig.json")
# firebase_admin.initialize_app(cred)


def create_app():
    app = Flask(__name__)
    app.secret_key = config.secret_key

    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
    )

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
