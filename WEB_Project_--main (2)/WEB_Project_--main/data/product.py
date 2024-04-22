import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'product'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True)
    delivery_date = sqlalchemy.Column(sqlalchemy.String)
    reviews = sqlalchemy.Column(sqlalchemy.String)
    src = sqlalchemy.Column(sqlalchemy.String, unique=True)
    kategory_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('kategory.id'), nullable=True)
    kategory = orm.relationship('Kategory')
