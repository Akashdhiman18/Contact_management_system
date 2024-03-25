from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
# Create A Model For Table
class Contacts(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(1000))
    last_name = db.Column(db.String(1000))
    email_address = db.Column(db.String(500))
    mobile = db.Column(db.String(30))
    home_address = db.Column(db.String(1000))
    url_of_picture = db.Column(db.String(1000))


class SystemUser(db.Model):
    __tablename__='registeruser'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(1000))
    emailaddress=db.Column(db.String(500))
    passcode=db.Column(db.String(500))
    mobileno=db.Column(db.String(30))

def __repr__(self):
        return f"<RegisterUser(name='{self.name}', email='{self.emailaddress}')>"

def check_password(self, password):
        return check_password_hash(self.passcode, password)
