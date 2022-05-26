from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint,render_template,redirect,url_for,flash,request
from werkzeug.security import generate_password_hash, check_password_hash
from project.models import Admin,Students,Important
from project.extensions import db 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired,Email, EqualTo, Length


auth = Blueprint('auth', __name__)

class Config(object):
    SECRET_KEY = 'my-secrete-key'   
class LoginForm(FlaskForm):
    user_name  = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    def __init__(self, user_name,password):
        self.user_name = user_name
        self.password = password
# Show Students Details
@auth.route('/show',methods=['GET','POST'])

def show():
    new_student=Students.query.all()
    flash('You have succesfully registered')
    return render_template('show.html',new_student=new_student)


@auth.route('/adminsignup')
def Asignup():
    return render_template('adminsignup.html')  

@auth.route('/adminsignup', methods=['GET','POST']) 
def adminsignup():   
    aname = request.form.get('aname')
    apaswd = request.form.get('apaswd')
    admin = Important.query.filter_by(aname=aname).first()
    if admin:
        flash("User already exist")
        return redirect (url_for('auth.adminlogin'))
    elif not admin:
        new_admin = Important(aname=aname,apaswd=apaswd)   
        db.session.add(new_admin)
        db.session.commit()
        return redirect (url_for('auth.adminlogin'))
    

@auth.route('/adminlogin')
def Alogin():
    return render_template('adminlogin.html')  

@auth.route('/adminlogin', methods= ['POST'])
def adminlogin():
    aname = request.form.get('aname')
    apaswd = request.form.get('apaswd')
    
    user = Important.query.filter_by(aname=aname).first()
    
    method, salt, hashval = user.apaswd.split("$", 2)
    print(apaswd)
    print(method)
    print(salt)
    print(hashval)
    print(check_password_hash(user.apaswd, apaswd))
    if user and check_password_hash(user.apaswd, apaswd):
        login_user(user)
        return redirect(url_for('auth.show'))
    return render_template('home.html')
    

    
 
@auth.route('/logout')
def logout():
    logout_user()
    return render_template('home.html')
  
  #---------------------------------------------------------------->
# @auth.route('/login', methods=['GET','POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.user_name.data == 'admin' and form.password.data == 'admin':
#             flash('login successful')
#             return redirect('index')
#     return render_template('login.html', form=form)