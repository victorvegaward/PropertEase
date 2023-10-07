import hashlib
import time


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

    @staticmethod
    def create_patient(first_name, last_name, phone_number, database):
        patient = Patient(first_name, last_name, phone_number)
        patient_document = patient.to_json()
        collection = database.patients
        collection.insert_one(patient_document)
        return patient

    def valid_first_name(self, first_name):
        if type(first_name) != str:
            raise TypeError("The patient's first name is not of type string")
        if len(first_name) > 25:
            raise ValueError("The patient's first name exceeds 25 characters")
        return first_name

    def valid_last_name(self, last_name):
        if type(last_name) != str:
            raise TypeError("The patient's last name is not of type string")
        if len(last_name) > 25:
            raise ValueError("The patient's last name exceeds 25 characters")
        return last_name

    def valid_phone_number(self, phone_number):
        if type(phone_number) != str:
            raise TypeError("Patient's phone number should be of type str")
        return phone_number

    def generate_patient_id(self):
        cur_time = str(time.time())
        hashed_time = hashlib.sha1()
        hashed_time.update(cur_time.encode("utf8"))
        return hashed_time.hexdigest()
    
    @staticmethod
    def get_patient_by_email(email, database):
        collection = database.patients
        patient_data = collection.find_one({"email": email})
        if patient_data:
            return Patient(patient_data['first_name'], patient_data['last_name'], patient_data['phone_number'])
        return None
