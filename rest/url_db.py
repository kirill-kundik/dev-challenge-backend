import trafaret as t
from bson import ObjectId
from trafaret.contrib.object_id import MongoId
from typing import List

url_keywords = t.Dict({
    t.Key('_id'): MongoId(),
    t.Key('url'): t.String(),
    t.Key('keywords'): t.List(t.String())
})


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
