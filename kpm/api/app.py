import os
from flask import Flask
import flask.ext.cors
from kpm.loghandler import init_logging


def create_app():
    app = Flask(__name__)
    flask.ext.cors.CORS(app)
    setting = os.getenv('APP_ENV', "development")

    if setting != 'production':
        app.config.from_object('kpm.api.config.DevelopmentConfig')
    else:
        app.config.from_object('kpm.api.config.ProductionConfig')
    from kpm.api.builder import builder_app
    from kpm.api.info import info_app
    from kpm.api.registry import registry_app
    app.register_blueprint(builder_app)
    app.register_blueprint(info_app)
    app.register_blueprint(registry_app)
    init_logging(app.logger, loglevel='INFO')
    app.logger.info("Start service")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0')