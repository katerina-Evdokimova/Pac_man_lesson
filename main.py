from const import SIZE_SP
from data_db import db_session
from game import Game


if __name__ == '__main__':
    # module =
    try:
        db_session.global_init("db/game.db")

        games = Game(2, SIZE_SP)
        games.start_screen()
    except Exception as e:
        print(e)

