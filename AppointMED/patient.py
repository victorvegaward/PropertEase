import hashlib
import time
import re


class Patient:

    def __init__(self, first_name, last_name, phone_number):
        self.first_name = self.valid_first_name(first_name)
        self.last_name = self.valid_last_name(last_name)
        self.phone_number = self.valid_phone_number(phone_number)
        self.patient_id = self.generate_patient_id()
        self.role = 'patient'

    def to_json(self):
        return {'first_name': self.first_name,
                'last_name': self.last_name,
                'phone_number': self.phone_number,
                'patient_id': self.patient_id,
                'role': self.role}
        
    # TODO REMOVE
    @staticmethod
    def create_patient(first_name, last_name, phone_number, database):
        patient = Patient(first_name, last_name, phone_number)
        patient_document = patient.to_json()
        collection = database.db.patients
        collection.insert_one(patient_document)
        return patient

    def valid_first_name(self, first_name):
        pattern = re.compile(r"^[A-Z][a-z'-]{1,24}$")
        if not pattern.match(first_name):
            raise ValueError("Invalid patient first name format")
        return first_name

    def valid_last_name(self, last_name):
        pattern = re.compile(r"^[A-Z][a-z'-]{1,24}$")
        if not pattern.match(last_name):
            raise ValueError("Invalid patient last name format")
        return last_name

    def valid_phone_number(self, phone_number):
        pattern = re.compile(
            r"^(?:\+?1[-.\s]?)?(\()?(\d{3})(?(1)\))[-.\s]?(\d{3})[-.\s]?(\d{4})$")
        if not pattern.match(phone_number):
            raise ValueError("Invalid patient phone number format")
        return phone_number

    # TODO REMOVE
    def generate_patient_id(self):
        cur_time = str(time.time())
        hashed_time = hashlib.sha1()
        hashed_time.update(cur_time.encode("utf8"))
        return hashed_time.hexdigest()

    @staticmethod
    def get_patient_by_email(email, mongo):
        user = mongo.db.users.find_one({"email": email, "role": "patient"})
        if user:
            patient_data = user["payload"]
            return Patient(patient_data['first_name'], patient_data['last_name'], patient_data['phone_number'])
        return None
