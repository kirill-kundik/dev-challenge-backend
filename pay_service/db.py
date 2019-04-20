from sqlalchemy import (
    MetaData, Table, Column, Integer, String
)

from pay_service.exceptions import PaymentNotFoundException

__all__ = ['payment']

meta = MetaData()

payment = Table(
    'payment', meta,

    Column('id', String(32), primary_key=True),
    Column('amount', Integer, nullable=False, default=1000),
    Column('user_ip', String(15), nullable=False)

)


async def get_payment(conn, pay_id):
    check = await conn.execute(
        payment.select().where(payment.c.id == pay_id)
    )
    res = await check.fetchone()
    if not res:
        raise PaymentNotFoundException
    return row2dict(res)


async def create_payment(conn, pay):
    stmt = payment.insert().values(id=pay['id'], user_ip=pay['user_ip'])
    await conn.execute(stmt)


async def proceed_payment(conn, pay):
    await get_payment(conn, pay['id'])  # check payment if exists
    stmt = payment.update().where(payment.c.id == pay['id']).values(amount=payment.c.amount - pay['amount'])
    await conn.execute(stmt)


async def check_payment(conn, pay_id):
    stmt = payment.select().where(payment.c.id == pay_id)
    res = await conn.execute(stmt)
    pay = await res.fetchone()
    if not pay:
        return False
    if pay['amount'] == 0:
        return True
    return False


def row2dict(row):
    d = {}
    for column in row:
        d[column] = row[column]

    return d
