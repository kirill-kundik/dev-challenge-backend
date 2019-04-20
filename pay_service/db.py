from sqlalchemy import (
    MetaData, Table, Column, Integer, String
)

__all__ = ['payment']

meta = MetaData()

payment = Table(
    'payment', meta,

    Column('id', String(32), primary_key=True),
    Column('amount', Integer, nullable=False, default=1000),
    Column('user_ip', String(15), nullable=False)

)
