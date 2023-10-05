import os
import certifi
from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask import flash, session, url_for
from appointment import Appointment
from doctor import Doctor
from event import Event
from user import User
from werkzeug.security import check_password_hash
import hashlib
import binascii



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

time_slots = ["08:00am", "08:30am", "09:00am", "09:30am", "10:00am", "10:30am", "11:00am", "11:30am", "12:00pm",
              "12:30pm", "01:00pm", "01:30pm", "02:00pm", "02:30pm", "03:00pm", "03:30pm", "04:00pm", "04:30pm"]

doctor_ids = {"Richard Silverstein": "1234"}

mongo = PyMongo(app, tlsCAFile=certifi.where())

bcrypt = Bcrypt(app)
# mongo.db.create_collection('doctors')

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    # Check if the user is logged in
    # if 'user_id' not in session:
    #     flash('Please login to access this page.', 'warning')
    #     return redirect(url_for('signin'))

    if request.method == "GET":
        doctors = Doctor.get_doctors(mongo)
    else:  # i.e., POST
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
    collection = mongo.db.events
    # collection.remove({})
    doc_id = doctor_ids["Richard Silverstein"]
    collection = mongo.db.events
    # event1 = Event.create_event("22/06/2022", "08:30am", "2423fe323", doc_id, mongo)
    event2 = Event.create_event("04/25/2022", "09:30am", "2423fe323", doc_id, mongo)
    event3 = Event.create_event("04/25/2022", "10:30am", "2423fe323", doc_id, mongo)
    event4 = Event.create_event("04/25/2022", "11:30am",  "2423fe323", doc_id, mongo)
    event5 = Event.create_event("04/25/2022", "01:30pm",  "2423fe323", doc_id, mongo)

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

# ... (other imports)
from flask_bcrypt import Bcrypt
from flask import flash, session, url_for


# Sign-Up Logic
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.get_user_by_email(email, mongo)
        # Testing
        hashed = hash_password("test2")
        print(f"Hashed: {hashed}")

        # Simulating stored password in DB
        stored_in_db = hashed

        # Verifying
        is_valid = verify_password(stored_in_db, "test2")
        print(f"Is Valid: {is_valid}")
        if user and verify_password(user.password, password):
            session['user_id'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            print("incorrect")
            flash('Login unsuccessful. Check email and password', 'danger')
    return render_template('Login.html')  # Assuming your HTML is named 'login.html'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first = request.form.get('first_name')
        last = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        specialties = request.form.getlist('specialties')
        hashed_password = hash_password(password)
        address = request.form.get('address')
        medical_coverages = request.form.getlist('medical_coverages')
        phone_number = request.form.get('phone_number')
        photo_url = request.form.get('photo_url')
        user = User.create_user(username=email, email=email, password=hashed_password, database=mongo.db)
        doctor = Doctor.create_doctor(first,last,specialties,address,0.0,0.0,medical_coverages,phone_number,photo_url,mongo.db)
        session['user_id'] = user.username
        flash('Account created!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html')  


@app.route('/signout')
def signout():
    """Handle user sign-out."""
    # Clear user's session
    session.clear()

    # Notify user they have been logged out
    flash('You have been logged out successfully!', 'success')

    # Redirect to home page
    return redirect(url_for('home'))


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2 and return the hexdigest."""
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), b'', 100000)
    return dk.hex()

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a password against its hashed version."""
    # Calculating the hash of the provided_password
    hashed_provided_password = hash_password(provided_password)

    return hashed_provided_password == stored_password