import sqlite3
from flask_login import UserMixin

DATABASE_PATH = "neon.db"  

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        """Retrieve a user from the database by ID."""
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        connection.close()

        if user:
            return User(
                id_=user[0],
                name=user[1],
                email=user[2],
                profile_pic=user[3],
            )
        return None

    @staticmethod
    def create(id_, name, email, profile_pic):
        """Create a new user in the database."""
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (id, name, email, profile_pic) VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )
        connection.commit()
        connection.close()
