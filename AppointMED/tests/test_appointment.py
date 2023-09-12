import unittest
from appointment import Appointment


class TestAppointment(unittest.TestCase):
    def setUp(self):
        self.appointment1 = Appointment("John Green", "doctorimage.com", "7874059898", "123 Street", "dermatologist",
                                        "123123123")
        self.appointment2 = Appointment("Guillermo Sanchez", "doctorimagewebsite.com","7874294698","Universal Studios Orlando",
                                        "neurologist", "asdfsadf")

    def test00_init(self):
        self.assertEqual(self.appointment1.name, "John Green")
        self.assertEqual(self.appointment1.doctor_image, "doctorimage.com")
        self.assertEqual(self.appointment1.phone, "7874059898")
        self.assertEqual(self.appointment1.specialty, "dermatologist")
        self.assertEqual(self.appointment1.doctor_id, "123123123")

        self.assertEqual(self.appointment2.name, "Guillermo Sanchez")
        self.assertEqual(self.appointment2.doctor_image, "doctorimagewebsite.com")
        self.assertEqual(self.appointment2.phone, "7874294698")
        self.assertEqual(self.appointment2.specialty, "neurologist")
        self.assertEqual(self.appointment2.doctor_id, "asdfsadf")

    def test01_setter_values(self):
        self.appointment1.set_doctor_name("Juan")
        self.assertEqual(self.appointment1.name, "Juan")
        self.appointment1.set_doctor_image("cnn.com")
        self.assertEqual(self.appointment1.doctor_image, "cnn.com")
        self.appointment1.set_doctor_phone("1234567890")
        self.assertEqual(self.appointment1.phone, "1234567890")
        self.appointment1.set_doctor_specialty("pediatrician")
        self.assertEqual(self.appointment1.specialty, "pediatrician")
        self.appointment1.set_doctor_id("123456789")
        self.assertEqual(self.appointment1.doctor_id, "123456789")

    def test02_setter_types(self):
        self.assertRaises(TypeError, Appointment, "John Green", False, "787877878", "123 Street", "dermatologist",
                          "123123123")
        self.assertRaises(TypeError, Appointment, "John Green", "doctorimage.com", 0.0, "123 Street", "dermatologist",
                          "123123123")
        self.assertRaises(TypeError, Appointment, "John Green", "doctorimage.com", "7874059898", 123, "dermatologist",
                          "123123123")
        self.assertRaises(TypeError, Appointment, "John Green", "doctorimage.com", "7874059898", "123 Street", 123,
                          "123123123")
        self.assertRaises(TypeError, Appointment, "John Green", "doctorimage.com", "7874059898", "123 Street",
                          "dermatologist", 123)
