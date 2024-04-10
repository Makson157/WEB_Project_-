import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    delivery_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    rewiews = sqlalchemy.Column(sqlalchemy.String, nullable=True)
