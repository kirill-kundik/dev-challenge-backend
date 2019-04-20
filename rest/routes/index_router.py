import asyncio

import aiohttp
import json

import bson
from aiohttp import web

from rest.url_db import *


class RoutesHandler:
    def __init__(self, mongo):
        self._mongo = mongo

    @property
    def mongo(self):
        return self._mongo

    async def _wait_for_keywords(self, url):
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.post('http://keywords:9002/', json={'url': url})
                keywords = await response.read()
                keywords = json.loads(keywords)
                if len(keywords) == 0:
                    await delete_by_url(self.mongo.url_keywords, url)
                else:
                    await update_url(self.mongo.url_keywords, url, keywords)
            except Exception as e:
                print(e)
                await delete_by_url(self.mongo.url_keywords, url)

    async def get_all(self, request):
        peername = request.transport.get_extra_info('peername')
        print(peername)
        if peername is not None:
            host, port = peername
            print(host, port)
        res = []
        async for document in self.mongo.url_keywords.find():
            res.append(doc_to_serializable(document))
        return web.Response(text=json.dumps(res))

    async def get_by_id(self, request):
        uid = request.query['id']
        try:
            res = await get_by_id(self.mongo.url_keywords, uid)
            if res:
                res = doc_to_serializable(res)
                status = 200
            else:
                res = 'This url is not found'
                status = 404
        except bson.errors.InvalidId as e:
            res = str(e)
            status = 400
        return web.Response(text=json.dumps(res), status=status)

    async def get_by_url(self, request):
        url = request.query['url']
        res = await get_by_url(self.mongo.url_keywords, url)
        if res:
            res = doc_to_serializable(res)
            status = 200
        else:
            res = 'This url is not found'
            status = 404
        return web.Response(text=json.dumps(res), status=status)

    async def insert_url(self, request):
        body = await request.json()
        url = body['url']
        check = await get_by_url(self.mongo.url_keywords, url)
        if check:
            return web.Response(status=400)
        res = await insert_url(self.mongo.url_keywords, url, [])
        asyncio.create_task(self._wait_for_keywords(url))
        return web.Response(text=str(res), status=201)

    async def update_url(self, request):
        body = await request.json()
        check = await get_by_url(self.mongo.url_keywords, body['url'])
        if not check:
            return web.Response(status=404)
        await update_url(self.mongo.url_keywords, body['url'], body['keywords'])
        return web.Response(status=200)

    async def delete_by_id(self, request):
        try:
            res = await delete_by_id(self.mongo.url_keywords, request.query['id'])
            if res:
                res = doc_to_serializable(res)
                status = 200
            else:
                res = 'This url is not found'
                status = 404
        except bson.errors.InvalidId as e:
            res = str(e)
            status = 400
        return web.Response(text=json.dumps(res), status=status)

    async def delete_by_url(self, request):
        res = await delete_by_url(self.mongo.url_keywords, request.query['url'])
        if res:
            res = doc_to_serializable(res)
            status = 200
        else:
            res = 'This url is not found'
            status = 404
        return web.Response(text=json.dumps(res), status=status)


def doc_to_serializable(doc):
    if len(doc['keywords']) == 0:
        return {doc['url']: 'Keywords for this url is under processing now!'}
    return {doc['url']: doc['keywords']}