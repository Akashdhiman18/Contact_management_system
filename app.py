
import os
import psycopg2
from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Contacts, SystemUser
from flask_migrate import Migrate
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime as dt


PROFILE_PIC_UPLOAD_FOLDER = 'static/img/contacts/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Init App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['PROFILE_PIC_UPLOAD_FOLDER'] = PROFILE_PIC_UPLOAD_FOLDER

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://domadmin:2021Shades@localhost:5432/contactsdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Function for file type validation
# Returns true if file to upload is of the type mentioned in ALLOWED_EXTENSIONS setting
def allowed_file(filename):
    # if file is user.jpg, it splits it at the '.' into two words -> user, jpg. It returns the second word i.e. jpg, 
    # converts it to lower case and checks if its in the ALLOWED_EXTENSIONS
    print("Here??")
    file_name_split = filename.rsplit('.', 1)
    print("Here too??")
    file_extension = file_name_split[1]
    print(file_extension)
    if file_extension in ALLOWED_EXTENSIONS:
        return True
    else:
        return False
    '''

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           '''

# function to get the file extension
def get_file_extension(filename):
    print("Here??")
    file_name_split = filename.rsplit('.', 1)
    print("Here too??")
    file_extension = file_name_split[1]
    print(file_extension)
    return file_extension

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
    contacts = Contacts.query.all()
    return render_template('users.html', contacts=contacts)

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
            #return render_template('users.html')
            output_msg = "Success."
            return jsonify({'output_msg': output_msg, 'success': True})
        else:
            output_msg = "Invalid email or password. Please try again."
            return jsonify({'output_msg': output_msg, 'success': False})

    # Return the 'login.html' template for GET requests
    print('does it get here - 2')
    return render_template('login.html')

    return render_template('users.html')

    # Return the 'register.html' template for GET requests
    return render_template('addcontact.html') 

@app.route('/addContact', methods=['POST','GET'])
def addContact():
    if request.method == "POST":
        firstnameData = request.form['firstname']
        lastnameData = request.form['lastname']
        emailaddressData = request.form['emailaddress']
        mobileData = request.form['mobilephone']
        homeaddressData = request.form['homeaddress']

        profile_pic_file_path = ""

        if 'file' in request.files:
            file = request.files['file']
            print(allowed_file(file.filename))

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print(filename)
                # Save the uploaded file as name of current time, first and last name
                dt_now = dt.now().strftime("%Y%m%d%H%M%S%f")
                file_extension = get_file_extension(file.filename)

                filename_to_save = firstnameData + "_" + lastnameData + "_" + dt_now + "." + file_extension
                print(filename_to_save)
                # Save this file to the folder path
                file.save(os.path.join(app.config['PROFILE_PIC_UPLOAD_FOLDER'], filename_to_save))
                profile_pic_file_path = PROFILE_PIC_UPLOAD_FOLDER + filename_to_save

       
        # pictureData = request.form['picture']
        try:

            new_contact = Contacts(
                first_name=firstnameData,
                last_name=lastnameData,
                email_address=emailaddressData,
                mobile=mobileData,
                home_address=homeaddressData,
                url_of_picture=profile_pic_file_path
            )
            db.session.add(new_contact)
            db.session.commit()
        
            output_msg = "Contact successfully added"
            return jsonify({'output_msg': output_msg, 'success': True})
        except:
            output_msg = "Whoops something went wrong while adding the contact. Try again later."
            return jsonify({'output_msg': output_msg, 'success': False})
    return render_template('addcontact.html')
   

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

        contacts = Contacts.query.all()
        return render_template('users.html', contacts=contacts)

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

        contacts = Contacts.query.all()
        return render_template('users.html', contacts=contacts)
        
    return "<h4>User delete page</h4>"



if __name__ == '__main__':
    app.run(debug=True)