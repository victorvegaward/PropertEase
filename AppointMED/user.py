from flask_bcrypt import Bcrypt
from bson import ObjectId


class User:
    def __init__(self, _id, email, password, role, payload):
        self._id = _id
        self.email = email
        self.password = password
        self.role = role
        self.payload = payload

    def to_json(self):
        return {
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "payload": self.payload
        }

    @staticmethod
    def create_user(bcrypt, email, password, role, payload, database):
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        user = User(None, email, hashed_password, role,
                    payload)
        user_document = user.to_json()
        collection = database["users"]
        inserted_id = collection.insert_one(user_document).inserted_id
        user._id = str(inserted_id)
        return user

    @staticmethod
    def get_user_by_email(email, database):
        collection = database["users"]
        user_document = collection.find_one({"email": email})

        if user_document:
            return User(str(user_document["_id"]), user_document["email"], user_document["password"], user_document["role"], user_document["payload"])
        else:
            return None
    
    @staticmethod
    def get_user_by_id(_id, database):
        collection = database["users"]
        user_document = collection.find_one({"_id": ObjectId(_id)})

        if user_document:
            return User(str(user_document["_id"]), user_document["email"], user_document["password"], user_document["role"], user_document["payload"])
        else:
            return None

    @staticmethod
    def check_password(bcrypt, stored_password, given_password):
        return bcrypt.check_password_hash(stored_password, given_password)
