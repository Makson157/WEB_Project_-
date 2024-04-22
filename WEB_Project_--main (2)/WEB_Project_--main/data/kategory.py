import sqlalchemy
from .db_session import SqlAlchemyBase


class Kategory(SqlAlchemyBase):
    __tablename__ = 'kategory'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
