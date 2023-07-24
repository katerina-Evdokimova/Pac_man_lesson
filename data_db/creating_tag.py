from data_db import db_session
from data_db.inf_game import InfGame
from data_db.stand_game import StandGame


def add_inf_game(score):
    inf_game = InfGame()
    inf_game.score = score
    db_sess = db_session.create_session()
    db_sess.add(inf_game)
    db_sess.commit()
    db_sess.close()


def add_stand_game(score, level):
    stand_game = StandGame()
    stand_game.score = score
    stand_game.level = level
    db_sess = db_session.create_session()
    db_sess.add(stand_game)
    db_sess.commit()
    db_sess.close()
