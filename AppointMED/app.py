import os
import certifi
from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from appointment import Appointment
from doctor import Doctor
from patient import Patient
from event import Event
from user import User
from dotenv import load_dotenv

load_dotenv()

# -- Initialization section --
app = Flask(__name__)
app.config["SECRET_KEY"] = "MedEasy"
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = 'MedEasy'

# name of database
app.config["MONGO_DBNAME"] = "MedEasy"

# URI of database
app.config[
    'MONGO_URI'] = "mongodb+srv://MedEasy:MedEasy@cluster0.l8xpye7.mongodb.net/MedEasy"

mongo = PyMongo(app, tlsCAFile=certifi.where())
bcrypt = Bcrypt(app)

time_slots = ["08:00am", "08:30am", "09:00am", "09:30am", "10:00am", "10:30am", "11:00am", "11:30am", "12:00pm",
              "12:30pm", "01:00pm", "01:30pm", "02:00pm", "02:30pm", "03:00pm", "03:30pm", "04:00pm", "04:30pm"]

doctor_ids = {"Richard Silverstein": "1234"}


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        users = mongo.db.users.find({"role": "doctor"})
    return render_template('home.html', users=users)



@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_email = session.get('email', None)
    user = User.get_user_by_email(user_email, mongo.db)

    if not user:  # Add this check to see if a user is returned.
        flash('User not found.', 'danger')
        return redirect(url_for('home'))

    if user.role == "doctor":
        if request.method == 'POST':

            first_name = request.form.get('first_name', user.first_name)
            last_name = request.form.get('last_name', user.last_name)
            specialties = request.form.getlist('specialties')
            address = request.form.get('address', user.address)
            phone_number = request.form.get(
                'phone_number', user.phone_number)
            medical_coverages = request.form.getlist('medical_coverages')
            
            collection = mongo.db.users
            collection.update_one({"email": user_email}, {
                "$set": {
                    "payload.first_name": first_name,
                    "payload.last_name": last_name,
                    "payload.specialties": specialties,
                    "payload.address": address,
                    "payload.phone_number": phone_number,
                    "payload.medical_coverages": medical_coverages
                }
            })
            # Refresh the user data after the update
            user = User.get_user_by_email(user_email, mongo.db)

        return render_template('doctor.html', doctor=user.payload)

    elif user.role == "patient":
        if request.method == 'POST':
            first_name = request.form.get(
                'first_name', user.payload['first_name'])
            last_name = request.form.get(
                'last_name', user.payload['last_name'])
            phone_number = request.form.get(
                'phone_number', user.payload['phone_number'])

            collection = mongo.db.users
            collection.update_one({"email": user_email}, {
                "$set": {
                    "payload.first_name": first_name,
                    "payload.last_name": last_name,
                    "payload.phone_number": phone_number
                }
            })
            user = User.get_user_by_email(user_email, mongo.db)

        return render_template('patient.html', patient=user.payload)

    else:
        flash('Invalid profile type.', 'danger')
        return redirect(url_for('home'))


@app.route("/Schedule/<doc_id>", methods=["GET", "POST"])
def schedule(doc_id):
    
    user = mongo.db.users.find_one({"user_id": doc_id, "role": "doctor"})
    doctor = user['payload']

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
        time_slots2 = Appointment.get_available_time_slots(
            doc_id, day, mongo, time_slots)
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
    collection = mongo.db.events
    # collection.remove({})
    doc_id = doctor_ids["Richard Silverstein"]
    collection = mongo.db.events
    # event1 = Event.create_event("22/06/2022", "08:30am", "2423fe323", doc_id, mongo)
    event2 = Event.create_event(
        "04/25/2022", "09:30am", "2423fe323", doc_id, mongo)
    event3 = Event.create_event(
        "04/25/2022", "10:30am", "2423fe323", doc_id, mongo)
    event4 = Event.create_event(
        "04/25/2022", "11:30am",  "2423fe323", doc_id, mongo)
    event5 = Event.create_event(
        "04/25/2022", "01:30pm",  "2423fe323", doc_id, mongo)

    collection = mongo.db.doctors
    Doctor.create_doctor("John", "Green", ['dermatologist', "allergist"],
                         "2925 Sycamore Dr # 204, Simi Valley, CA 93065, United States", 18.368650, -66.053291,
                         ["United Health", "Triple S"], "787-689-9012",
                         "https://totalcommercial.com/photos/1/206401-resized.jpg", mongo)
    doctor1 = Doctor.create_doctor("Damaris", "Torres", ["neurologist"], "San Juan, P.R.", 18.466333, -66.105721,
                                   ["Triple S", "Medicaid"], "787-777-7776", 'url()', mongo)
    doctor1 = Doctor.create_doctor(" Jose", "Rodriguez", ["dermatologist"], "Rio Grande, P.R.", 18.38023, -65.83127,
                                   ["Triple S"], "787-776-7776", 'url()', mongo)
    doctor1 = Doctor.create_doctor("Pedro", "Figueroa", ["allergist"], "Mayaguez, P.R.", 18.20107, -67.139627,
                                   ["Medicaid"], "787-576-7776", 'url()', mongo)

    return "seeded successfully"


@app.route('/signin', methods=['GET'])
def signinGET():
    return render_template('signin.html')

@app.route('/signin', methods=['POST'])
def signinPOST():
    email = request.form.get('email')
    password = request.form.get('password')
    user = mongo.db["users"].find_one({"email": email})
    print(user)
    print(password)
    print(user.get('password'))

    if user and User.check_password(bcrypt, user.get('password'), password):
        session["user_id"] = user.get('user_id')
        session['user_role'] = user.get('role')
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Login unsuccessful. Check email and password', 'danger')
    return signinGET()


@app.route('/signup', methods=['GET'])
def signupGET():
    return render_template('signup.html')
    
@app.route('/signup', methods=['POST'])
def signupPOST():
    account_type = request.form.get('accountType')
    email = request.form.get('email')

    # 1. Check if the email already exists in the database
    existing_user = mongo.db["users"].find_one({"email": email})

    if existing_user:
    # 2. If the email exists, flash an error message
        flash('An account with that email already exists!', 'danger')
        return signupGET()

    # Continue with the rest of the signup process if email is unique
    password = request.form.get('password')

    payload = {}

    # Fields specific to the doctor role
    if account_type == "patient":
            payload["first_name"] = request.form.get('patient_first_name')
            payload["last_name"] = request.form.get('patient_last_name')
            payload["phone_number"] = request.form.get('patient_phone_number')

    if account_type == "doctor":
            payload["first_name"] = request.form.get('first_name')
            payload["last_name"] = request.form.get('last_name')
            payload["specialties"] = request.form.getlist('specialties')
            payload["address"] = request.form.get('address')
            payload["medical_coverages"] = request.form.getlist(
                'medical_coverages')
            payload["phone_number"] = request.form.get('phone_number')

    # Create the user with the above payload
    created_user = User.create_user(bcrypt, email=email, password=password,
                                        role=account_type, payload=payload, database=mongo.db)

    session['user_id'] = created_user.user_id
    session['user_role'] = account_type
    flash('Account created!', 'success')
    return redirect(url_for('home'))


@app.route('/signout')
def signout():
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('home'))

