from flask_bcrypt import Bcrypt


class User:
    def __init__(self, user_id, email, password, role, payload):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.role = role
        self.payload = payload

    def to_json(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "payload": self.payload
        }

    @staticmethod
    def create_user(bcrypt, email, password, role, payload, database):
        # Generate unique user_id here
        user_id_prefix = "DOC_" if role == "doctor" else "PAT_"
        # Fetch the last created user's ID and increment the number
        last_user = list(database["users"].find().sort("_id", -1).limit(1))
        last_id = 0 if not last_user else int(
            last_user[0]["user_id"].split('_')[1])
        user_id = user_id_prefix + str(last_id + 1).zfill(3)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(user_id, email, hashed_password, role, payload)
        user_document = user.to_json()
        collection = database.db["users"]
        collection.insert_one(user_document)
        return user

    @staticmethod
    def get_user_by_email(email, database):
        collection = database.db["users"]
        user_document = collection.find_one({"email": email})

        if user_document:
            return User(user_document["user_id"], user_document["email"], user_document["password"], user_document["role"], user_document["payload"])
        else:
            return None

    @staticmethod
    def check_password(bcrypt, stored_password, given_password):
        return bcrypt.check_password_hash(stored_password, given_password)
