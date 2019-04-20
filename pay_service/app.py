import sys
import logging

from aiohttp import web

from pay_service.db import payment
from pay_service.routes import config_routes
from pay_service.utils import get_config
from postgres.db_init import init_db
from postgres.db_start import init_pg, close_pg


async def init_app(argv=None):
    app = web.Application()

    app['config'] = get_config(argv)

    # setup Jinja2 template renderer
    # aiohttp_jinja2.setup(
    #     app, loader=jinja2.PackageLoader('app', 'templates'))

    # create db connection on startup, shutdown on exit
    app.on_startup.append(init_pg)
    # app.on_startup.append(init_security)
    app.on_cleanup.append(close_pg)

    config_routes(app)

    return app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    init_db([payment])

    app = init_app(argv)

    config = get_config(argv)
    web.run_app(app,
                host=config['host'],
                port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
