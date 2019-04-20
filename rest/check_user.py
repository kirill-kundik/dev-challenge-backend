from rest.db import get_user_by_ip, set_user_pay_id
from rest.payments import create_payment, get_payment_info


async def check_user(user_collection, user_ip, url_id):
    user = await get_user_by_ip(user_collection, user_ip)
    if user['last_pay_id'] is not None and user['last_pay_id'] != '':
        pay_id = user['last_pay_id']
        res = {
            'payment_link': 'http://0.0.0.0:9003/?pay_id=' + pay_id,
            'payment_info': await get_payment_info(pay_id),
            'available_at': 'http://0.0.0.0:9001/getWithCheck?pay_id=' + pay_id + '&id=' + str(
                url_id) + '&ip=' + user_ip,
            'how_to_pay':
                'Send a POST request to http://0.0.0.0/9003 with json {pay_id = your_payment_id, amount = 1000}'
        }
    else:
        pay_id = await create_payment(user_ip)
        await set_user_pay_id(user_collection, user_ip, pay_id)
        res = {
            'payment_link': 'http://0.0.0.0:9003/?pay_id=' + pay_id,
            'payment_info': await get_payment_info(pay_id),
            'available_at': 'http://0.0.0.0:9001/getWithCheck?pay_id=' + pay_id + '&id=' + str(
                url_id) + '&ip=' + user_ip,
            'how_to_pay':
                'Send a POST request to http://0.0.0.0/9003 with json {pay_id = your_payment_id, amount = 1000}'
        }
    return res
