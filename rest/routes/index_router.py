import asyncio

import aiohttp
import json

import bson
from aiohttp import web

from rest.check_user import check_user
from rest.payments import check_payment
from rest.db import *


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

    async def get_with_check(self, request):
        if 'pay_id' not in request.query or 'id' not in request.query or 'ip' not in request.query:
            return web.HTTPBadRequest()
        pay_id = request.query['pay_id']
        url_id = request.query['id']
        url = await get_by_id(self.mongo.url_keywords, url_id)
        user_ip = request.query['ip']
        if await check_payment(pay_id):
            await add_url_to_user(self.mongo.user, user_ip, url['url'])
            res = doc_to_serializable(url)
            return web.Response(text=json.dumps(res))
        return web.Response(text='You have not paid!')

    async def get_all(self, request):
        user_ip = get_request_ip(request)
        if user_ip is None:
            return web.HTTPBadRequest()
        res = []

        for document in await get_all_user_urls(self.mongo.user, self.mongo.url_keywords, user_ip):
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
        user_ip = get_request_ip(request)
        if user_ip is None:
            return web.HTTPBadRequest
        url = request.query['url']
        try:
            res = await get_keywords_for_user(self.mongo.user, self.mongo.url_keywords, user_ip, url)
            res = doc_to_serializable(res)

        except Exception:
            url_id = await get_by_url(self.mongo.url_keywords, url)
            if url_id:
                url_id = url_id['_id']
                res = await check_user(self.mongo.user, user_ip, url_id)
            else:
                res = None
        if res:
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
        print('NEW URL ADDED, ITS ID: ')
        print(res)
        asyncio.create_task(self._wait_for_keywords(url))
        return web.Response(status=201)

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


def get_request_ip(request):
    peername = request.transport.get_extra_info('peername')
    if peername is not None:
        host, port = peername
        print(host)
        return host
    return None
