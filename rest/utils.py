import os
import motor.motor_asyncio as aiomotor

import argparse
import pathlib

from trafaret_config import commandline

import trafaret as T

TRAFARET = T.Dict({
    T.Key('mongo'):
        T.Dict({
            'host': T.String(),
            'port': T.Int(),
            'database': T.String(),
            'max_pool_size': T.Int()
        }),
    T.Key('host'): T.IP,
    T.Key('port'): T.Int(),
})

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'config.yml'


def get_config(argv=None):
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=DEFAULT_CONFIG_PATH
    )

    # ignore unknown options
    options, unknown = ap.parse_known_args(argv)

    config = commandline.config_from_options(options, TRAFARET)
    return config


async def init_mongo(conf, loop):
    host = os.environ.get('DOCKER_MACHINE_IP', 'db')
    conf['host'] = host
    mongo_uri = "mongodb://{}:{}".format(conf['host'], conf['port'])
    conn = aiomotor.AsyncIOMotorClient(
        mongo_uri,
        maxPoolSize=conf['max_pool_size'],
        io_loop=loop)
    db_name = conf['database']
    return conn[db_name]
