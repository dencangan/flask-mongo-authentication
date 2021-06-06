"""
Module to contain objects for the app.
"""
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config


class User(object):
    """
    User object that can be manipulated with mongo.
    The collection name is 'user_details'.
    """

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
        # Your mongo URI defined in config.py
        self.db = MongoClient(Config.MONGO_URI)["Users"]

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @classmethod
    def set_password(cls, password):
        """Hashing the password with Werkzeug hash generator."""
        cls.password_hash = generate_password_hash(password)

    @staticmethod
    def check_password(hashed_password, password):
        """Validating the hashed password."""
        return check_password_hash(hashed_password, password)

    def get_by_username(self, username):
        """Getting user details by username."""
        return self.db["user_details"].find_one({"name": username})

    def register(self):
        """Inserting user details into mongo collection."""
        self.db["user_details"].insert_one(self.to_dict())
        print(f"{self.to_dict()} entry created.")

    def to_dict(self):
        """Transform to dict to insert into mongo collection."""
        return {
            "name": self.username,
            "email": self.email,
            # Storing hashed password, you should NEVER store the password itself in the database
            "password": self.password_hash,
        }
