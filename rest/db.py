import datetime
from time import struct_time, strftime, strptime, localtime

import trafaret as t
from bson import ObjectId
from trafaret.contrib.object_id import MongoId
from typing import List

url_keywords = t.Dict({
    t.Key('_id'): MongoId(),
    t.Key('url'): t.String(),
    t.Key('keywords'): t.List(t.String())
})

user = t.Dict({
    t.Key('_id'): MongoId(),
    t.Key('user_ip'): t.String(),
    t.Key('next_trial'): t.String(),
    t.Key('urls'): t.List(t.String()),
    t.Key('last_pay_id'): t.String()
})


def convert_time_to_str(time: struct_time) -> str:
    return strftime("%Y-%m-%d %H:%M:%S", time)


def convert_str_to_time(s: str) -> struct_time:
    return strptime(s, "%Y-%m-%d %H:%M:%S")


def plus_one_day():
    now = datetime.datetime.utcnow()
    plus_day = now + datetime.timedelta(days=1)
    return plus_day.timetuple()


async def get_all_user_urls(user_collection, url_collection, user_ip):
    curr_user = await user_collection.find_one({
        'user_ip': user_ip
    })
    result = []
    if curr_user:
        urls = curr_user['urls']
        for url in urls:
            result.extend((await get_by_url(url_collection, url))['keywords'])
    return result


async def add_url_to_user(user_collection, user_ip, url):
    curr_user = await user_collection.find_one({
        'user_ip': user_ip,
    })
    urls = curr_user['urls']
    urls.append(url)
    await user_collection.update_one({
        'user_ip': user_ip
    }, {
        '$set': {
            'urls': urls,
            'last_pay_id': None
        }
    })


async def get_keywords_for_user(user_collection, url_collection, user_ip, url):
    curr_user = await user_collection.find_one({
        'user_ip': user_ip
    })
    if curr_user:
        if convert_str_to_time(curr_user['next_trial']) <= localtime():
            new_urls = curr_user['urls']
            new_urls.append(url)
            await user_collection.update_one({
                'user_ip': user_ip
            }, {
                '$set': {'next_trial': convert_time_to_str(plus_one_day()),
                         'urls': new_urls}
            })
            return await get_by_url(url_collection, url)
        else:
            raise Exception
    else:
        await user_collection.insert_one({
            'user_ip': user_ip,
            'next_trial': convert_time_to_str(plus_one_day()),
            'urls': [url],
            'last_pay_id': None
        })
        return await get_by_url(url_collection, url)


async def set_user_pay_id(user_collection, user_ip, pay_id):
    await user_collection.update_one({
        'user_ip': user_ip
    }, {
        '$set': {'last_pay_id': pay_id}
    })


async def get_user_by_ip(user_collection, user_ip):
    res = await user_collection.find_one({
        'user_ip': user_ip
    })
    return res if res else None


async def get_all(url_collection):
    return await url_collection.find()


async def get_by_url(url_collection, url: str):
    res = await url_collection.find_one({
        'url': url
    })
    return res if res else None


async def get_by_id(url_collection, uid):
    res = await url_collection.find_one({
        '_id': ObjectId(uid)
    })
    return res if res else None


async def insert_url(url_collection, url: str, keywords: List[str]) -> int:
    res = await url_collection.insert_one({'url': url, 'keywords': keywords})
    return res.inserted_id


async def update_url(url_collection, url: str, keywords: List[str]) -> None:
    await url_collection.update_one({
        'url': url
    }, {
        '$set': {'keywords': keywords}
    })


async def delete_by_url(url_collection, url: str):
    res = await get_by_url(url_collection, url)
    await url_collection.delete_many({
        'url': url
    })
    return res if res else None


async def delete_by_id(url_collection, uid):
    res = await get_by_id(url_collection, uid)
    await url_collection.delete_many({
        '_id': ObjectId(uid)
    })
    return res if res else None
