from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# Create A Model For Table
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(1000))
    last_name = db.Column(db.String(1000))
    email_address = db.Column(db.String(500))
    mobile = db.Column(db.String(30))
    home_address = db.Column(db.String(1000))
    url_of_picture = db.Column(db.String(1000))

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    access_code = db.Column(db.Integer)
    email_address = db.Column(db.String(500))