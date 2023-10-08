import hashlib
import time
import re


class Doctor:

    curr_specialties = {'dermatologist', 'allergist',
                        'cardiologist', 'gastroenterologist', 'neurologist'}

    def __init__(self, first_name, last_name, specialties, address, lat, lng, medical_coverages, phone_number, photo_url):
        self.first_name = self.valid_first_name(first_name)
        self.last_name = self.valid_last_name(last_name)
        self.specialties = self.valid_specialties(specialties)
        self.address = self.valid_address(address)
        self.lat = self.valid_lat(lat)
        self.lng = self.valid_lng(lng)
        self.medical_coverages = self.valid_medical_coverages(
            medical_coverages)
        self.phone_number = self.valid_phone_number(phone_number)
        self.photo_url = self.valid_photo_url(photo_url)
        self.doc_id = self.generate_doctor_id()
        self.role = 'doctor'

    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'specialties': self.specialties,
            'address': self.address,
            'lat': self.lat,
            'lng': self.lng,
            'medical_coverages': self.medical_coverages,
            'phone_number': self.phone_number,
            'photo_url': self.photo_url,
            'doc_id': self.doc_id,
            'role': self.role
        }

    @staticmethod
    def create_doctor(first_name, last_name, specialties, address, lat, lng, medical_coverages, phone_number, photo_url, database):
        doctor = Doctor(first_name, last_name, specialties, address,
                        lat, lng, medical_coverages, phone_number, photo_url)
        doctor_document = doctor.to_json()
        collection = database.db.doctors
        collection.insert_one(doctor_document)
        return doctor

    @staticmethod
    def get_doctors(mongo):
        return mongo.doctors.find()


    @staticmethod
    def get_filtered_doctors(database, specialty, name):
        collection = database.db.doctors  # Fixed collection assignment
        if not specialty and not name:
            return collection.find()
        elif not specialty:
            return collection.aggregate([{'$search': {'index': 'name', 'text': {'query': name, 'path': {'wildcard': '*'}}}}])
        elif not name:
            return collection.find({'specialties': specialty})
        name_filter = collection.aggregate(
            [{'$search': {'index': 'name', 'text': {'query': name, 'path': {'wildcard': '*'}}}}])
        result = []
        for doctor in name_filter:
            add = True
            for spty in doctor['specialties']:
                if spty != specialty:
                    add = False
            if add:
                result.append(doctor)
        return result

    def valid_first_name(self, first_name):
        pattern = re.compile(r"^[A-Z][a-z'-]{1,24}$")
        if not pattern.match(first_name):
            raise ValueError("Invalid doctor first name format")
        return first_name

    def valid_last_name(self, last_name):
        pattern = re.compile(r"^[A-Z][a-z'-]{1,24}$")
        if not pattern.match(last_name):
            raise ValueError("Invalid doctor last name format")
        return last_name

    def valid_specialties(self, specialties):
        if type(specialties) != list:
            raise TypeError("The doctor's specialties is not of type list")
        for specialty in specialties:
            if type(specialty) != str:
                raise TypeError("The doctor's specialty is not of type string")
            if specialty not in Doctor.curr_specialties:
                raise ValueError(f"{specialty} is not a valid specialty.")
        return specialties

    def valid_address(self, address):
        if type(address) != str:
            raise TypeError("The doctor's address is not of type str")
        return address

    def valid_lat(self, lat):
        if type(lat) != float:
            raise TypeError("The the doctor's office latitude cordinate is not of type float")
        if lat <= -91.0 or lat >= 90.0:
            raise ValueError("The Doctor's office latitude cordinate is not in range of [-90 to 90].")
        return lat
            
    def valid_lng(self, lng):
        if type(lng) != float:
            raise TypeError("The the doctor's office latitude cordinate is not of type float")
        if lng <= -181.0 or lng >= 181.0:
            raise ValueError("The Doctor's office latitude cordinate is not in range of [-180 to 180].")
        return lng
    
    def valid_medical_coverages(self, medical_coverages):
        if type(medical_coverages) != list:
            raise TypeError("Medical coverages should be of type list")
        
        for coverage in medical_coverages:
            if type(coverage) != str:
                raise TypeError("Medical coverage should be of type str")
    
        return medical_coverages

    def valid_phone_number(self, phone_number):
        pattern = re.compile(
            r"^(?:\+?1[-.\s]?)?(\()?(\d{3})(?(1)\))[-.\s]?(\d{3})[-.\s]?(\d{4})$")
        if not pattern.match(phone_number):
            raise ValueError("Invalid doctor phone number format")
        return phone_number

    def valid_photo_url(self, photo_url):
        pattern = re.compile(r'^(http|https)://')
        if not pattern.match(photo_url):
            raise ValueError("Invalid doctor photo URL format")
        return photo_url

    def generate_doctor_id(self):
        cur_time = str(time.time())
        hashed_time = hashlib.sha1()
        hashed_time.update(cur_time.encode("utf8"))
        return hashed_time.hexdigest()