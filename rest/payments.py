import json

import aiohttp


async def check_payment(pay_id):
    async with aiohttp.ClientSession() as session:
        response = await session.get('http://pay_service:9003/check?pay_id=' + pay_id)
        pay_info = await response.read()
        pay_info = json.loads(pay_info)

        return pay_info['success']


async def get_payment_info(pay_id):
    async with aiohttp.ClientSession() as session:
        response = await session.get('http://pay_service:9003/?pay_id=' + pay_id)
        pay_info = await response.read()
        pay_info = json.loads(pay_info)

        return pay_info


async def create_payment(user_ip):
    async with aiohttp.ClientSession() as session:
        response = await session.post('http://pay_service:9003/', json={'user_ip': user_ip})
        pay_id = await response.read()
        pay_id = json.loads(pay_id)

        return pay_id
