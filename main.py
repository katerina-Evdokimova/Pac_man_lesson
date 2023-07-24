from const import SIZE_SP
from data_db import db_session
from game import Game


db_session.global_init("db/game.db")

games = Game(2, SIZE_SP)
games.start_screen()

