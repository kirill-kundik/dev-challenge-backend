import logging
import pathlib
import asyncio

from aiohttp import web

from routes import RoutesHandler, setup_routes
from utils import init_mongo, load_config

PROJ_ROOT = pathlib.Path(__file__).parent.parent


async def setup_mongo(app, conf, loop):
    mongo = await init_mongo(conf['mongo'], loop)

    async def close_mongo(app):
        mongo.client.close()

    app.on_cleanup.append(close_mongo)
    return mongo


async def init(loop):
    conf = load_config(PROJ_ROOT / 'config' / 'config.yml')
    app = web.Application()
    mongo = await setup_mongo(app, conf, loop)

    handler = RoutesHandler(mongo)
    setup_routes(app, handler)
    host, port = conf['host'], conf['port']

    return app, host, port


def main():
    # logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
