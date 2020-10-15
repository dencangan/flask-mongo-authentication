"""Module to contain objects for the app."""

from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo


class User:
    """User object that can be manipulated with mongo."""

    def __init__(self, username, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

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

    @classmethod
    def get_by_username(cls, username):
        """Getting user details by username."""
        return mongo.db.user_details.find_one({"name": username})

    def register(self):
        """Inserting user details into mongo collection."""
        mongo.db.user_details.insert_one(self.to_dict())
        print(f"{self.to_dict()} entry created.")

    def to_dict(self):
        """Transform to dict to insert into mongo collection."""
        return {
            "name": self.username,
            "email": self.email,
            # Storing hashed password, you should NEVER store the password itself in the database
            "password": self.password_hash,
        }
