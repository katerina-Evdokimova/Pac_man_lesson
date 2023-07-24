import datetime

import sqlalchemy
from sqlalchemy import orm

from data_db.db_session import SqlAlchemyBase


class StandGame(SqlAlchemyBase):
    __tablename__ = 'stand_game'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    level = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def __repr__(self):
        return f'<StandGame> {self.id} | {self.level} | {self.score} | {self.create_date}'

