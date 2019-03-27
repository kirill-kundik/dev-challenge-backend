import os
import motor.motor_asyncio as aiomotor

import yaml


def load_config(fname):
    with open(fname, 'rt') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data


async def init_mongo(conf, loop):
    host = os.environ.get('DOCKER_MACHINE_IP', '127.0.0.1')
    conf['host'] = host
    mongo_uri = "mongodb://{}:{}".format(conf['host'], conf['port'])
    conn = aiomotor.AsyncIOMotorClient(
        mongo_uri,
        maxPoolSize=conf['max_pool_size'],
        io_loop=loop)
    db_name = conf['database']
    return conn[db_name]
