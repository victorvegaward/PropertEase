import unittest
from event import Event


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.event1 = Event("01/12/2022", "12:00pm", "8eaee45fb99a7e0d1321db82f71ab314c9fda74c", "test")
        self.event2 = Event("31/12/2043", "4:30pm", "8eaee45fb99a7e0d1321db82f71ab314c9fda74c", "123123")
        self.event3 = Event("01/1/2024", "8:00am", "8eaee45fb99a7e0d1321db82f71ab314c9fda74c", "testtest")

    def test00_init(self):
        self.assertEqual(self.event1.get_date(), "01/12/2022")
        self.assertEqual(self.event1.get_start_time(), "12:00pm")
        self.assertEqual(self.event1.get_appointment_id(), "8eaee45fb99a7e0d1321db82f71ab314c9fda74c")
        self.assertEqual(self.event1.get_doctor_id(), "test")

        self.assertEqual(self.event2.get_date(), "31/12/2043")
        self.assertEqual(self.event2.get_start_time(), "4:30pm")
        self.assertEqual(self.event2.get_appointment_id(), "8eaee45fb99a7e0d1321db82f71ab314c9fda74c")
        self.assertEqual(self.event2.get_doctor_id(), "123123")

        self.assertEqual(self.event3.get_date(), "01/1/2024")
        self.assertEqual(self.event3.get_start_time(), "8:00am")
        self.assertEqual(self.event3.get_appointment_id(), "8eaee45fb99a7e0d1321db82f71ab314c9fda74c")
        self.assertEqual(self.event3.get_doctor_id(), "testtest")

    def test01_init_types(self):
        self.assertRaises(TypeError, Event, False, "12:00pm", "8eaee45fb99a7e0d1321db82f71ab314c9fda74c", "test")
        self.assertRaises(TypeError, Event, "01/12/2022", False, "8eaee45fb99a7e0d1321db82f71ab314c9fda74c", "test")
        self.assertRaises(TypeError, Event, "01/12/2022", "12:00pm", False, "test")
        self.assertRaises(TypeError, Event, "01/12/2022", "12:00pm", "8eaee45fb99a7e0d1321db82f71ab314c9fda74c", False)

    def test02_init_values(self):
        self.assertRaises(ValueError, Event, "00/12/2022", "12:00pm", "8eaee45fb99a7e0d1321db82f71ab314c9fda74c",
                          "test")
        self.assertRaises(ValueError, Event, "01/00/2022", "12:00pm", "8eaee45fb99a7e0d1321db82f71ab314c9fda74c",
                          "test")
        self.assertRaises(ValueError, Event, "01/32/2022", "12:00pm", "8eaee45fb99a7e0d1321db82f71ab314c9fda74c",
                          "test")

    def test03_str(self):
        self.assertEqual(str(self.event1),
                         "date: 01/12/2022, start_time: 12:00pm, appointment_id: "
                         "8eaee45fb99a7e0d1321db82f71ab314c9fda74c, doctor_id: test")
        self.assertEqual(str(self.event2),
                         "date: 31/12/2043, start_time: 4:30pm, appointment_id: "
                         "8eaee45fb99a7e0d1321db82f71ab314c9fda74c, doctor_id: 123123")
        self.assertEqual(str(self.event3),
                         "date: 01/1/2024, start_time: 8:00am, appointment_id: "
                         "8eaee45fb99a7e0d1321db82f71ab314c9fda74c, doctor_id: testtest")

    def test04_to_json(self):
        self.assertEqual(self.event1.to_json(), {"date": "01/12/2022", "start_time": "12:00pm",
                                                 "appointment_id": "8eaee45fb99a7e0d1321db82f71ab314c9fda74c",
                                                 "doctor_id": "test"})
        self.assertEqual(self.event2.to_json(), {"date": "31/12/2043", "start_time": "4:30pm",
                                                 "appointment_id": "8eaee45fb99a7e0d1321db82f71ab314c9fda74c",
                                                 "doctor_id": "123123"})
        self.assertEqual(self.event3.to_json(), {"date": "01/1/2024", "start_time": "8:00am",
                                                 "appointment_id": "8eaee45fb99a7e0d1321db82f71ab314c9fda74c",
                                                 "doctor_id": "testtest"})
