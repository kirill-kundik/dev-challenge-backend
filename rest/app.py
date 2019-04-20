import pathlib
import asyncio

from aiohttp import web

from rest.routes.config import setup_routes
from rest.routes.index_router import RoutesHandler
from rest.utils import init_mongo, get_config

PROJ_ROOT = pathlib.Path(__file__).parent.parent


async def setup_mongo(app, conf, loop):
    mongo = await init_mongo(conf['mongo'], loop)

    async def close_mongo(app):
        mongo.client.close()

    app.on_cleanup.append(close_mongo)
    return mongo


async def init(loop):
    conf = get_config()
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
    print('Web service initialized')
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
