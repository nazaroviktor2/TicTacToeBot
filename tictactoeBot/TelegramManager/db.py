import logging
import os
import psycopg2 as psycopg2

from exception import NotFoundGame, BoardAlreadyExist, NotFoundBoard

DATABASE = os.getenv('POSTGRES_DB')
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
HOST = os.getenv("POSTGRES_DB_HOST")
PORT = "5432"

def create_user(user_id, user_name):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM users WHERE id = {user_id}")
        if cur.fetchone() is None:

            cur.execute(f"INSERT INTO users (id, name) VALUES (%s, %s)", (user_id, user_name))
            logging.info(f"User with id = {user_id} successfully registered")
        else:
            logging.info(f"User with id = {user_id} already registered")


def create_game(user_id, open_game: bool):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()

        cur.execute(f"INSERT INTO games(first_id, open_game) VALUES ({user_id}, {open_game}) RETURNING id;")
        game_id = cur.fetchone()[0]
        logging.info(f"game id = {game_id}")
    # insert_user_and_game(user_id, game_id)
    return game_id


def delete_game(id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM games WHERE id = '{id}'")
        if cur.fetchone() is None:
            logging.error(f"Game with id =  {id} not found ")
            raise NotFoundGame(f"Game with id =  {id} not found ")
        else:
            cur.execute(f"DELETE FROM games WHERE id = '{id}'")
            logging.info(f"Game with id =  {id} deleted")


def find_open_game():
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute("SElECT id from games where second_id is Null and status = 'find players' and open_game = True ")
        return cur.fetchone()


def get_game_code_by_id(id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT secret_code FROM games WHERE id = {id}")
        if cur.fetchone() is None:
            logging.error(f"Game with id =  {id} not found ")
            raise NotFoundGame(f"Game with id =  {id} not found ")
        else:
            cur.execute(f"SELECT secret_code FROM games WHERE id = {id}")
            return cur.fetchone()[0]


def get_game_id_by_code(code: str):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM games WHERE secret_code = '{code}' ")
        if cur.fetchone() is None:
            logging.error(f"Game with code =  {code} not found ")
            raise NotFoundGame(f"Game with code =  {code} not found ")
        else:
            cur.execute(f"SELECT id FROM games WHERE secret_code = '{code}'")
            return cur.fetchone()[0]


# Adding the id of the second player
def update_game_second_id(id, second_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id from games WHERE id = {id}")
        if cur.fetchone is None:
            raise NotFoundGame(f"Game with id = {id} not found")
        else:
            cur.execute(f"UPDATE games SET second_id = {second_id} WHERE id = {id}")


def get_players_id(game_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id from games WHERE id = {game_id}")
        if cur.fetchone() is None:
            raise NotFoundGame(f"Game with id = {game_id} not found")
        else:
            cur.execute(f"SELECT first_id, second_id  FROM games WHERE id = {game_id}")
            return cur.fetchone()


def create_board(id, cross_id, zero_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id from games WHERE id = {id}")
        if cur.fetchone() is None:
            raise NotFoundGame(f"Game with id = {id} not found")

        cur.execute(f"SELECT id from  boards WHERE id = {id}")
        if cur.fetchone() is None:
            cur.execute(f"INSERT INTO boards(id, cross_id, zero_id) VALUES (%s, %s, %s)", (id, cross_id, zero_id))
        else:
            raise BoardAlreadyExist(f" Board with id = {id} already exist")


def get_board_by_id(id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id from  boards WHERE id = {id}")
        if cur.fetchone() is None:
            raise NotFoundBoard(f" Board with id = {id} not found")
        else:
            cur.execute(f"SELECT one, two, three, four, five, six, seven, eight, nine from boards WHERE id = {id}")
            return cur.fetchone()


def get_board_zero_id(board_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id from  boards WHERE id = {board_id}")
        if cur.fetchone() is None:
            raise NotFoundBoard(f" Board with id = {board_id} not found")
        else:
            cur.execute(f"SELECT zero_id from boards WHERE id = {board_id}")
            return cur.fetchone()[0]


def get_board_cross_id(board_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id from  boards WHERE id = {board_id}")
        if cur.fetchone() is None:
            raise NotFoundBoard(f" Board with id = {board_id} not found")
        else:
            cur.execute(f"SELECT cross_id from boards WHERE id = {board_id}")
            return cur.fetchone()[0]


def update_board(board_id, position, value):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id from  boards WHERE id = {board_id}")
        if cur.fetchone() is None:
            raise NotFoundBoard(f" Board with id = {board_id} not found")
        else:
            cur.execute(f"UPDATE boards SET {position} = '{value}' WHERE id = {board_id}")


def get_user_name(id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id from users WHERE id = {id}")
        if cur.fetchone() is None:
            raise NotFoundGame(f"User with id = {id} not found")
        else:
            cur.execute(f"SELECT name from users WHERE id = {id}")
            return cur.fetchone()[0]


def get_first_role(id_game):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id from games WHERE id = {id_game}")
        if cur.fetchone is None:
            raise NotFoundGame(f"Game with id = {id_game} not found")
        else:
            cur.execute(f"SELECT role_first_player from games WHERE id = {id_game}")
            return cur.fetchone()[0]


def get_second_role(id_game):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id from games WHERE id = {id_game}")
        if cur.fetchone is None:
            raise NotFoundGame(f"Game with id = {id_game} not found")
        else:
            cur.execute(f"SELECT role_second_player from games WHERE id = {id_game}")
            return cur.fetchone()[0]


def get_game_status(id_game):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT status from games WHERE id = {id_game}")
        if cur.fetchone() is None:
            raise NotFoundGame(f"Game with id = {id_game} not found")
        else:
            cur.execute(f"SELECT status from games WHERE id = {id_game}")
            return cur.fetchone()[0]


def set_game_status_starting(id_game):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT set_game_status_starting({int(id_game)})")


def set_game_status_finished(id_game):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT set_game_status_finished({int(id_game)})")


def set_game_status_player_joining(id_game):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"SELECT set_game_status_player_joining({int(id_game)})")


def game_set_winner(game_id, user_id):
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(f"UPDATE games SET winner = {user_id} WHERE id = {game_id}")


def init_database():
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT) as con:
        cur = con.cursor()
        cur.execute(open("init.sql", "r").read())

# def insert_user_and_game(user_id, game_id):
#     with psycopg2.connect(
#             database=DATABASE,
#             user=USER,
#             password=PASSWORD,
#             host=HOST,
#             port=PORT) as con:
#         cur = con.cursor()
#         cur.execute(f"INSERT INTO user_and_game(user_id, game_id) VALUES (%s, %s)", (user_id, game_id))
