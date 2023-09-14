import os
import certifi
from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo

from appointment import Appointment
from doctor import Doctor
from event import Event

# -- Initialization section --
app = Flask(__name__)

# name of database
app.config["MONGO_DBNAME"] = "PropertEase"

# URI of database
app.config[
    'MONGO_URI'] = "mongodb+srv://PropertEase:PropertEase@cluster0.zc1kdsn.mongodb.net/PropertEase"

time_slots = ["08:00am", "08:30am", "09:00am", "09:30am", "10:00am", "10:30am", "11:00am", "11:30am", "12:00pm",
              "12:30pm", "01:00pm", "01:30pm", "02:00pm", "02:30pm", "03:00pm", "03:30pm", "04:00pm", "04:30pm"]

doctor_ids = {"Richard Silverstein": "1234"}

mongo = PyMongo(app, tlsCAFile=certifi.where())


# mongo.db.create_collection('doctors')

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        doctors = Doctor.get_doctors(mongo)
    else:
        specialty = request.form['doctor-specialty']
        name = request.form['doctor-name']
        doctors = Doctor.get_filtered_doctors(mongo, specialty, name)
    return render_template("home.html", doctors=doctors)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/Schedule/<doc_id>", methods=["GET", "POST"])
def schedule(doc_id):
    collection = mongo.db.doctors
    doctor = collection.find_one({'doc_id': doc_id})

    medical_plans = doctor['medical_coverages']
    doctor_name = doctor['first_name'] + " " + doctor['last_name']
    doctor_image = doctor['photo_url']
    specialties = doctor['specialties']
    address = doctor['address']
    phone = doctor['phone_number']

    if request.form == "GET":
        time_slots2 = []
        time = ''

        # time_slots= Appointment.get_available_time_slots(doc_id,"04-22-2022",mongo)
        return render_template("appointment.html", day='', time_slots=time_slots2,
                               doctor_image=doctor_image,
                               doctor_name=doctor_name, doctor_specialty=specialties,
                               doctor_address=address,
                               doctor_phone=phone, medical_plans=medical_plans)
    else:
        day = str(request.form.get('day'))
        time = ''
        time = request.form.get('time')
        appt_id = Appointment.generate_appointment_id()
        collection = mongo.db.events
        time_slots2 = Appointment.get_available_time_slots(doc_id, day, mongo, time_slots)
        if time:
            day = request.form.get('day2')
            print(day)
            Event.create_event(day, time, appt_id, doc_id, mongo)
            return redirect("/" + appt_id)
        return render_template("appointment.html", day=day, time_slots=time_slots2,
                               doctor_image=doctor_image,
                               doctor_name=doctor_name, doctor_specialty=specialties,
                               doctor_address=address,
                               doctor_phone=phone, medical_plans=medical_plans)


@app.route("/<appt_id>")
def confirmed_event(appt_id):
    event = Event.get_event(appt_id, mongo)
    date = event.get_date()
    start_time = event.get_start_time()
    appointment_id = event.get_appointment_id()

    return render_template("event.html", date=date, start_time=start_time, appointment_id=appointment_id)


@app.route("/seed_db")
def seed_db():
    # collection = mongo.db.events
    # collection.remove({})
    doc_id = doctor_ids["Richard Silverstein"]
    # collection = mongo.db.events
    event1 = Event.create_event("22-06-2022", "08:30am", "2423fe323", doc_id, mongo)
    event2 = Event.create_event("09:30am", "04/25/2022", "2423fe323", doc_id, mongo)
    event3 = Event.create_event("10:30am", "04/25/2022", "2423fe323", doc_id, mongo)
    event4 = Event.create_event("11:30am", "04/25/2022", "2423fe323", doc_id, mongo)
    event5 = Event.create_event("01:30pm", "04/25/2022", "2423fe323", doc_id, mongo)

    collection = mongo.db.doctors
    Doctor.create_doctor("John", "Green", ['dermatologist', "allergist"],
                         "2925 Sycamore Dr # 204, Simi Valley, CA 93065, United States", 18.368650, -66.053291,
                         ["United Health", "Triple S"], 7876899012,
                         "https://totalcommercial.com/photos/1/206401-resized.jpg", mongo)
    doctor1 = Doctor.create_doctor("Damaris", "Torres", ["neurologist"], "San Juan, P.R.", 18.466333, -66.105721,
                                   ["Triple S", "Medicaid"], "787-777-7776", 'url()', mongo)
    doctor1 = Doctor.create_doctor(" Jose", "Rodriguez", ["dermatologist"], "Rio Grande, P.R.", 18.38023, -65.83127,
                                   ["Triple S"], "787-776-7776", 'url()', mongo)
    doctor1 = Doctor.create_doctor("Pedro", "Figueroa", ["allergist"], "Mayaguez, P.R.", 18.20107, -67.139627,
                                   ["Medicaid"], "787-576-7776", 'url()', mongo)

    return "seeded successfully"

@app.route("/SignIn")
def sign_in():
    return render_template("Login-Template.html")