class Event:
    def __init__(self, date: str, start_time: str, appointment_id: str, doctor_id: str):
        """
        Initializes Event object
        :param start_time: Time event starts
        :param date: Date event takes place
        :param appointment_id: ID of appointment associated with event
        :param doctor_id: ID of doctor associated with event
        """
        self.date = None
        self.start_time = None
        self.appointment_id = None
        self.doctor_id = None
        self.set_date(date)
        self.set_start_time(start_time)
        self.set_appointment_id(appointment_id)
        self.set_doctor_id(doctor_id)

    def __str__(self):
        """
        Method returns a string representation of the Event object
        :return: String representation of Event object
        """
        return f"date: {self.date}, start_time: {self.start_time}, appointment_id: {self.appointment_id}, " \
               f"doctor_id: {self.doctor_id}"

    # Setters
    def set_date(self, date: str):
        if type(date) != str:
            raise TypeError("date must be a string")
        date_elements = date.split("/")
        day = date_elements[1]
        month = date_elements[0]
        year = date_elements[2]
        if int(day) <= 0 or int(day) >= 32:
            raise ValueError("date is invalid")
        if int(month) <= 0 or int(month) >= 13:
            raise ValueError("date is invalid")
        if int(year) <= 2000 or int(year) >= 3000:
            raise ValueError("date is invalid")
        self.date = date

    def set_start_time(self, start_time: str):
        if type(start_time) != str:
            raise TypeError("start_time must be a string")
        self.start_time = start_time

    def set_appointment_id(self, appointment_id: str):
        if type(appointment_id) != str:
            raise TypeError("appointment_id must be a string")
        if len(appointment_id) != 40:
            raise ValueError("appointment_id must be 40 characters long")
        self.appointment_id = appointment_id

    def set_doctor_id(self, doctor_id: str):
        if type(doctor_id) != str:
            raise TypeError("doctor_id must be a string")
        self.doctor_id = doctor_id

    # Getters
    def get_date(self):
        return self.date

    def get_start_time(self):
        return self.start_time

    def get_appointment_id(self):
        return self.appointment_id

    def get_doctor_id(self):
        return self.doctor_id

    ###
    def to_json(self):
        """
        Method returns every class property as a JSON
        :return: dictionary of properties and class values
        """
        return {
            "date": self.date,
            "start_time": self.start_time,
            "appointment_id": self.appointment_id,
            "doctor_id": self.doctor_id
        }

    @staticmethod
    def create_event(date: str, start_time: str, appointment_id: str, doctor_id: str, database):
        """
        Method returns an event object and stores it in a mongoDB database
        :param start_time: Time event starts
        :param date: Date event takes place
        :param appointment_id: ID of appointment associated with event
        :param doctor_id: ID of doctor associated with event
        :param database: MongoDB database
        :return: Event object
        """
        event = Event(date, start_time, appointment_id, doctor_id)
        event_document = event.to_json()
        collection = database.db.events
        collection.insert_one(event_document)
        return event

    @staticmethod
    def get_event(appointment_id: str, database):
        """
        Method returns an event object from a mongoDB database
        :param appointment_id: ID of appointment associated with event
        :param database: MongoDB database
        :return: Event object
        """
        collection = database.db.events
        event_document = collection.find_one({"appointment_id": appointment_id})
        return Event(event_document["date"], event_document["start_time"], event_document["appointment_id"],
                     event_document["doctor_id"])
