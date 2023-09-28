from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        
    def to_json(self):
        """
        Convert the User object to JSON format for database storage.
        """
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def create_user(username, email, password, database):
        """
        Create a new User object and store it in the MongoDB database.
        """
        user = User(username, email, password)
        user_document = user.to_json()
        collection = database.db.users
        collection.insert_one(user_document)
        return user

    @staticmethod
    def get_user_by_email(email, database):
        """
        Fetch a user from the MongoDB database by their email.
        """
        collection = database.db.users
        user_document = collection.find_one({"email": email})

        if user_document:
            return User(user_document["username"], user_document["email"], user_document["password"])
        return None

    @staticmethod
    def validate_login(stored_password, given_password):
        """
        Validate the password provided during login.
        """
        return check_password_hash(stored_password, given_password)
