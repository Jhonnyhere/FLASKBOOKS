from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint,render_template,redirect,url_for,flash,request
from werkzeug.security import generate_password_hash, check_password_hash
from project.models import Admin,Students,Important
from project.extensions import db 


auth = Blueprint('auth', __name__)


# Show Students Details
@auth.route('/show',methods=['GET','POST'])

def show():
    new_student=Students.query.all()
    flash('You have succesfully registered')
    return render_template('show.html',new_student=new_student)

# SignUp
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
        new_admin = Important(aname=aname,apaswd=generate_password_hash(apaswd, method="sha256"))   
        db.session.add(new_admin)
        db.session.commit()
        return redirect (url_for('auth.adminlogin'))
    
# Login
@auth.route('/adminlogin')
def Alogin():
    return render_template('adminlogin.html')  

@auth.route('/adminlogin', methods= ['GET','POST'])
def adminlogin():
    aname = request.form.get('aname')
    apaswd = request.form.get('apaswd')
    
    admin = Important.query.filter_by(aname=aname).first()

    if  admin and check_password_hash(admin.apaswd, apaswd):
        return redirect(url_for('auth.show'))
        
    else:
    
      return redirect(url_for('main.gallery'))
    
 
@auth.route('/logout')
def logout():
    logout_user()
    return render_template('home.html')
  
    