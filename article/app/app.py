from functools import lru_cache

from sanic import Sanic, Blueprint
from sanic_openapi import openapi3_blueprint

from article.views import articles, users
from config import setup_database, shutdown_database, DefaultSettings, get_base_settings


@lru_cache
def get_app(settings: DefaultSettings = None):
    settings = get_base_settings(settings)
    app = Sanic(settings.app_name)
    app.ctx.settings = settings
    api = Blueprint.group([articles, users], url_prefix="/app")
    app.blueprint(api)
    app.blueprint(openapi3_blueprint)

    @app.listener('after_server_start')
    async def setup_app(app, loop):
        app.ctx.engine, app.ctx.session = setup_database(settings)

    @app.listener('after_server_stop')
    async def shutdown_application(app, loop):
        await shutdown_database(app)

    return app


app = get_app()
