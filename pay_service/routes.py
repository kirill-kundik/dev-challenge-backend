# routes.py
import uuid
import logging
from aiohttp import web
import pay_service.db as db
from pay_service.exceptions import DatabaseException


async def check_payment(request):
    pay_id = request.rel_url.query['pay_id']
    user_ip = request.rel_url.query['user_ip']
    async with request.app['db'].acquire() as conn:
        try:
            res = await db.check_payment(conn, pay_id, user_ip)
        except DatabaseException:
            res = False
        return web.json_response({'success': res})


async def get_payment(request):
    if 'pay_id' in request.rel_url.query:
        pay_id = request.rel_url.query['pay_id']
        async with request.app['db'].acquire() as conn:
            try:
                res = await db.get_payment(conn, pay_id)
                return web.json_response(res)
            except DatabaseException:
                return web.HTTPBadRequest()
    return web.HTTPBadRequest()


async def proceed_payment(request):
    body = await request.json()
    if 'pay_id' not in body or 'amount' not in body:
        return web.HTTPBadRequest()
    pay = {
        'id': body['pay_id'],
        'amount': int(body['amount'])
    }
    async with request.app['db'].acquire() as conn:
        try:
            await db.proceed_payment(conn, pay)
            return web.json_response({'success': True})
        except DatabaseException:
            return web.HTTPBadRequest()


async def create_payment(request):
    body = await request.json()
    pay_id = uuid.uuid4().hex
    pay = {
        'id': pay_id,
        'user_ip': body['user_id']
    }
    async with request.app['db'].acquire() as conn:
        await db.create_payment(conn, pay)
        return web.json_response({'pay_id': pay_id})


def config_routes(app):
    router = app.router

    router.add_route('POST', '/', create_payment, name='create')
    router.add_route('GET', '/check', check_payment, name='check')
    router.add_route('POST', '/proceed', proceed_payment, name='proceed')
    router.add_route('GET', '/', get_payment, name='get')
