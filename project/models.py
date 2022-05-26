from project.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class Important(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aname = db.Column(db.String(50), nullable=False, unique=True)
    apaswd = db.Column(db.String(100), nullable=False)
    
    def __init__(self,aname,apaswd):
        self.aname=aname
        self.apaswd=generate_password_hash(apaswd)
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String(50), nullable=False)
    image = db.Column(db.Text, nullable = False)
    filename = db.Column(db.Text)
    mimetype = db.Column(db.Text, nullable = False)
    date = db.Column(db.Date)
    
    def __init__(self,location,image,date,mimetype,filename=filename):
        self.location = location
        self.image = image
        self.date = date
        self.mimetype = mimetype
        self.filename = filename
class Students(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    father_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable= False)
    dob = db.Column(db.Date)
    standard = db.Column(db.String(50))
    
    
    def __init__(self,name,father_name,dob,standard,email):
        self.name = name
        self.father_name = father_name
        self.dob = dob
        self.email =email
        self.standard = standard
        
class Admin(UserMixin,db.Model):
    id =  db.Column(db.Integer,  primary_key=True)
    uname = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(50), nullable = False) 
    
    def __init__(self,uname,password):
        self.uname= uname
        self.password = password        
