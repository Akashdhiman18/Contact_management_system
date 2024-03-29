from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
# Create A Model For Table
class Contacts(db.Model):
    __tablename__ = 'contacts'
    contact_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(1000))
    last_name = db.Column(db.String(1000))
    email_address = db.Column(db.String(500))
    mobile = db.Column(db.String(30))
    home_address = db.Column(db.String(1000))
    url_of_picture = db.Column(db.String(1000))
    
    def __repr__(self):
        return f"Contacts('{self.first_name}', '{self.last_name}', '{self.email_address}')"


class SystemUser(db.Model):
    __tablename__='systemuser'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email_address = db.Column(db.String(500))
    passcode = db.Column(db.String(500))
    mobile_no = db.Column(db.String(30))
    
    def __repr__(self):
        return f"SystemUser('{self.name}', '{self.email_address}')"

