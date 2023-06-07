import re
from helpers import select_puzzle, menu, register_player, play_game
class Player:

    def __init__(self, username, id=None):
        self.username = username
        self.id = id
    #TODO need to add regex for special characters
    def __repr__(self):
        return (f"<Username: {self.username}>")

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if (isinstance(username, str) 
            and 1 <= len(username) <= 8 
            and not hasattr(self, '_username')
            and re.match(r"^[a-zA-Z0-9]+$", username)
            ):
            self._username = username
        else:
            raise AttributeError('username must be a string between 1 and 8 characters and cannot be recreated')

    def handle_new_player(self, username):
        CURSOR.execute("SELECT * FROM players WHERE username = ?", (username,))
        check_username = CURSOR.fetchone()
        if check_username is None:
            Player.create_player(username)
            print(f"Hi there, {username}!")
            ready_to_play = input("Ready to play? Y/N: ")
            if ready_to_play.upper() == "Y":
                # select_puzzle()
                selected_puzzle_dummy_test = Puzzle("Puzzle1", "snake")
                play_game(self, selected_puzzle_dummy_test)
            else:
                menu()
        else:
            print('That username is taken try another one')
            register_player()

    def validate_user(self, username):
        CURSOR.execute("SELECT * FROM players WHERE username = ?", (username,))
        check_username = CURSOR.fetchone()
        if check_username is None:
            print('That username does not exist create the new username then start game')
            register_player()
        else:
            # current_player = Player.find_by_username(username)
            print(f"Welcome back {username}")
            ready_to_play = input("Ready to play? Y/N: ")
            if ready_to_play.upper() == "Y":
                select_puzzle()
            else:
                menu()

    def get_scores(self, puzzle):
        # validate that puzzle is a puzzle
        # return player's scores for this puzzle
        return [result.score for result in Result.get_all() if result.player_id == self.id]

    @classmethod
    def create_table(cls): 
        sql = """
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                username TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    def update(self):
        CURSOR.execute(
            """
            UPDATE players
            SET username = ?
            WHERE id = ?
        """,
            (self.username,),
        )
        CONN.commit()
        return type(self).find_by_id(self.id)

    def save(self):
        CURSOR.execute(
            """
            INSERT INTO players (username)
            VALUES (?);
        """,
            (self.username,),
        )
        CONN.commit()
        self.id = CURSOR.lastrowid

    def delete(self):
        CURSOR.execute(
            """
            DELETE FROM players
            WHERE id = ?
        """,
            (self.id,),
        )
        CONN.commit()
        return self

    @classmethod
    def create_player(cls, username):
        new_player = cls(username)
        new_player.save()
        return new_player

    @classmethod
    def get_all(cls):
        CURSOR.execute(
            """
                SELECT * FROM players;
            """
        )
        rows = CURSOR.fetchall()
        return [cls(row[1], row[0]) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute(
            """
            SELECT * FROM players
            WHERE id is ?;
        """,
            (id,),
        )
        row = CURSOR.fetchone()
        return cls(row[1], row[0]) if row else None

    @classmethod
    def drop_table(cls):
        CURSOR.execute(
            """
            DROP TABLE IF EXISTS players;
        """
        )
        CONN.commit()

    @classmethod
    def find_by_username(cls, username):
        CURSOR.execute(
            """
            SELECT * FROM players
            WHERE username is ?;
        """,
            (username,),
        )
        row = CURSOR.fetchone()
        return cls(row[1], row[0]) if row else None

from .__init__ import CONN, CURSOR 
from classes.puzzle import Puzzle
from classes.result import Result