import asyncio

import aiohttp
import json

import bson
from aiohttp import web

from db import *


class RoutesHandler:
    def __init__(self, mongo):
        self._mongo = mongo

    @property
    def mongo(self):
        return self._mongo

    async def _wait_for_keywords(self, url):
        async with aiohttp.ClientSession() as session:
            response = await session.post('keywords/', json={'url': url})
            keywords = await response.json()
            await update_url(self.mongo.url_keywords, url, keywords)

    async def get_all(self, request):
        res = []
        async for document in self.mongo.url_keywords.find():
            res.append(doc_to_serializable(document))
        return web.Response(text=json.dumps(res))

    async def get_by_id(self, request):
        uid = request.query['id']
        try:
            res = await get_by_id(self.mongo.url_keywords, uid)
            res = doc_to_serializable(res) if res else 'This url is not found'
        except bson.errors.InvalidId as e:
            res = str(e)
        return web.Response(text=json.dumps(res), status=200)

    async def get_by_url(self, request):
        url = request.query['url']
        res = await get_by_url(self.mongo.url_keywords, url)
        res = doc_to_serializable(res) if res else 'This url is not found'
        return web.Response(text=json.dumps(res), status=200)

    async def insert_url(self, request):
        body = await request.json()
        url = body['url']
        res = await insert_url(self.mongo.url_keywords, body['url'], [])
        asyncio.create_task(self._wait_for_keywords(url))
        return web.Response(text=str(res))

    async def update_url(self, request):
        body = await request.json()
        await update_url(self.mongo.url_keywords, body['url'], body['keywords'])

    async def delete_by_id(self, request):
        try:
            res = await delete_by_id(self.mongo.url_keywords, request.query['id'])
            res = doc_to_serializable(res) if res else 'This url is not found'
        except bson.errors.InvalidId as e:
            res = str(e)
        return web.Response(text=json.dumps(res))

    async def delete_by_url(self, request):
        res = await delete_by_url(self.mongo.url_keywords, request.query['url'])
        res = doc_to_serializable(res) if res else 'This url is not found'
        return web.Response(text=json.dumps(res))


def doc_to_serializable(doc):
    if len(doc['keywords']) == 0:
        return {doc['url']: 'Keywords for this url is under processing now!'}
    return {doc['url']: doc['keywords']}


def setup_routes(app, handler):
    router = app.router
    h = handler
    router.add_get('/getAll', h.get_all)
    router.add_get('/getByUrl', h.get_by_url)
    router.add_get('/getById', h.get_by_id)
    router.add_post('/add', h.insert_url)
    router.add_put('/update', h.update_url)
    router.add_delete('/deleteById', h.delete_by_id)
    router.add_delete('/deleteByUrl', h.delete_by_url)
