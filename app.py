
import os
import psycopg2
from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Contacts, SystemUser
from flask_migrate import Migrate
from werkzeug.security import check_password_hash

# Init App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:dhiman223@localhost:5432/contactsdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)
app.config['STATIC_FOLDER'] = 'static'
# Routes
@app.route('/', methods=['GET'])
def index():
    usersdata = Contacts.query.order_by(Contacts.contact_id).all()
    return render_template('home.html', usersdata=usersdata)

@app.route('/users', methods=['GET'])
def users():
    usersdata = Contacts.query.order_by(Contacts.contact_id).all()
    return render_template('users.html', usersdata=usersdata)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        mobileno = request.form['mobileno']

        # Check if password and confirm_password match
        if password != confirm_password:
            return "Passwords do not match. Please try again."

        # Check if the email is already registered
        existing_user = SystemUser.query.filter_by(email_address=email).first()
        if existing_user:
            return "Email address is already registered."

        # Create a new user
        new_user = SystemUser(name=name, email_address=email, passcode=password, mobile_no=mobileno)
        db.session.add(new_user)
        db.session.commit()

        return "Registration successful!"

    # Return the 'register.html' template for GET requests
    return render_template('register.html')

@app.route('/register-by-ajax', methods=['GET', 'POST'])
def register_user_by_ajax():
    if request.method == "POST":
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        mobileno = request.form['mobileno']
        output_msg = ""

        # Check if password and confirm_password match
        if password != confirm_password:
            output_msg = "Passwords do not match. Please try again."
            return jsonify({'output_msg': output_msg})

        # Check if the email is already registered
        existing_user = SystemUser.query.filter_by(email_address=email).first()
        if existing_user:
            output_msg = "Email address is already registered."
            return jsonify({'output_msg': output_msg})

        # Create a new user
        new_user = SystemUser(name=name, email_address=email, passcode=password, mobile_no=mobileno)
        db.session.add(new_user)
        db.session.commit()

        output_msg = "Registration successful!"
        return jsonify({'output_msg': output_msg})

    # Return the 'register.html' template for GET requests
    return render_template('register.html')


@app.route('/login-by-ajax', methods=['GET', 'POST'])
def login_by_ajax():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        output_msg = ""

        # Check if the email exists in the database
        user = SystemUser.query.filter_by(email_address=email).first()
        if user and user.passcode == password:
            print('does it get here - 1')
            # return "Login successful!"
            return render_template('users.html')
        else:
            output_msg = "Invalid email or password. Please try again."
            return jsonify({'output_msg': output_msg})

    # Return the 'login.html' template for GET requests
    print('does it get here - 2')
    return render_template('login.html')

# @app.route('/addContact', methods=['GET', 'POST'])
# def addContact():
#     if request.method == "POST":
#         firstnameData = request.form['firstname']
#         lastnameData = request.form['lastname']
#         emailaddressData = request.form['emailaddress']
#         mobileData = request.form['mobilephone']
#         homeaddressData = request.form['homeaddress']
#         pictureData = request.form['picture']

#         newUser = Users(first_name=firstnameData, last_name=lastnameData, email_address=emailaddressData, 
#                         mobile=mobileData, home_address=homeaddressData, url_of_picture=pictureData)
#         db.session.add(newUser)
#         db.session.commit()
#         return render_template('users.html')

#     # Return the 'register.html' template for GET requests
#     return render_template('addContacts.html')

   

@app.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == "GET":
        userid = request.args.get('ID')
        userdata = Contacts.query.filter_by(id=userid).first()
        return render_template('edit.html', userdata=userdata)
    elif request.method == "POST":
        userid = request.args.get('ID')
        userdatatochange = Contacts.query.filter_by(id=userid).first()
       
        updatedhomeaddressofuser = request.form['homeaddress']
        updatedfirstnameofuser = request.form['firstname']
        updatedemailaddressofuser = request.form['emailaddress']

        userdatatochange.home_address = updatedhomeaddressofuser
        userdatatochange.first_name = updatedfirstnameofuser
        userdatatochange.email_address = updatedemailaddressofuser
        db.session.commit()

        return "<h1>" + userdatatochange.email_address + "</h1>"

@app.route('/deletecheck', methods=['POST', 'GET'])
def deletecheck():
    if request.method == "GET":
        userid = request.args.get('ID')
        userdata = Contacts.query.filter_by(id=userid).first()
        return render_template('delete_check.html', userdata=userdata)
    return "<h4>User delete page</h4>"

@app.route('/deleteproceed', methods=['GET', 'POST'])
def deleteproceed():
    if request.method == "GET":
        userid = request.args.get('ID')
        userdata = Contacts.query.filter_by(id=userid).first()

        db.session.delete(userdata)
        db.session.commit()

        usersdata = Contacts.query.order_by(Contacts.id).all()
        return render_template('users.html', usersdata=usersdata)
        
    return "<h4>User delete page</h4>"



if __name__ == '__main__':
    app.run(debug=True)