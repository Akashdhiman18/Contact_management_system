
import os
import psycopg2
from flask import Flask, redirect, render_template, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Users, registeruser
from flask_migrate import Migrate
from werkzeug.security import check_password_hash

# Init App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://domadmin:2021Shades@localhost:5432/contactsdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)
app.config['STATIC_FOLDER'] = 'static'
# Routes
@app.route('/', methods=['GET'])
def index():
    usersdata = Users.query.order_by(Users.id).all()
    return render_template('home.html', usersdata=usersdata)

@app.route('/users', methods=['GET'])
def users():
    usersdata = Users.query.order_by(Users.id).all()
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
        existing_user = registeruser.query.filter_by(emailaddress=email).first()
        if existing_user:
            return "Email address is already registered."

        # Create a new user
        new_user = registeruser(name=name, emailaddress=email, passcode=password, mobileno=mobileno)
        db.session.add(new_user)
        db.session.commit()

        return "Registration successful!"

    # Return the 'register.html' template for GET requests
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # Check if the email exists in the database
        user = registeruser.query.filter_by(emailaddress=email).first()
        if user and user.passcode == password:
            return "Login successful!"
        else:
            return "Invalid email or password. Please try again."

    # Return the 'login.html' template for GET requests
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
        userdata = Users.query.filter_by(id=userid).first()
        return render_template('edit.html', userdata=userdata)
    elif request.method == "POST":
        userid = request.args.get('ID')
        userdatatochange = Users.query.filter_by(id=userid).first()
       
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
        userdata = Users.query.filter_by(id=userid).first()
        return render_template('delete_check.html', userdata=userdata)
    return "<h4>User delete page</h4>"

@app.route('/deleteproceed', methods=['GET', 'POST'])
def deleteproceed():
    if request.method == "GET":
        userid = request.args.get('ID')
        userdata = Users.query.filter_by(id=userid).first()

        db.session.delete(userdata)
        db.session.commit()

        usersdata = Users.query.order_by(Users.id).all()
        return render_template('users.html', usersdata=usersdata)
        
    return "<h4>User delete page</h4>"



if __name__ == '__main__':
    app.run(debug=True)