from flask_login import login_required
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from project.extensions import db
from werkzeug.utils import secure_filename
import os
from project.models import Product,Students

main = Blueprint('main', __name__)

Upload_Folder = "project/static/pictures"

# Home page 
@main.route('/')
def home():
    return render_template("home.html")
# Camp info
@main.route('/camps')
def camps():
    return render_template('camps.html')
# News
@main.route('/news')
def news():
    return render_template('news.html')

# Add data of Camps Location
@main.route('/add_any')
@login_required
def add():
    return render_template('add_product.html')

@main.route('/add_any',methods=['POST'])
@login_required
def add_any():
    pic = request.files["pic"]
    if not pic:
        return 'no pic uploaded'
    
    location = request.form.get('location')
    pic_name = secure_filename(pic.filename)
    mimetype = pic.mimetype
    date = request.form.get('date')
    if not pic_name or not mimetype:
        return 'bad upload',400
    pic.save(os.path.join(Upload_Folder, pic_name))
   
    file_path = './static/pictures/'+pic_name
    product = Product(location=location,date=date,image=file_path,mimetype=mimetype,filename=pic_name)
    db.session.add(product)
    db.session.commit()
    product_det = Product.query.all()
    return render_template('gallery.html',product_det=product_det)

# To show Camp Data
@main.route('/gallery',methods=['POST','GET'])
def gallery():
    product_det = Product.query.all()
    flash('data has been uploaded')
    return render_template('gallery.html',product_det=product_det)

# Students REgistration
@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/register', methods=['GET','POST'])
def register_user():
    name = request.form.get('name')
    father_name = request.form.get('father_name')
    dob = request.form.get('dob')
    email = request.form.get('email')
    standard = request.form.get('standard')
    
    student = Students.query.filter_by(email=email).first()
                                      
    if student:
        flash('You have already registered or try using other email')
        return redirect(url_for('main.register'))
    
    new_student = Students(name=name,email=email,dob=dob,standard=standard,father_name=father_name)
    
    db.session.add(new_student)
    db.session.commit()
    
    return 'You have succesfully registered'



# Show Camp Details
@main.route('/list',methods=['GET'])
def list():
    product_det = Product.query.all()
    return render_template('list.html',product_det=product_det)

# Edit or Update Camps Details
@main.route('/<int:id>/edit',methods=['POST','GET'])
def edit(id):
    product_det = Product.query.filter_by(id=id).first()
    if not product_det:
        return "Invalid request"
    if request.method=="POST":
       
            pic = request.files["pic"]
            
            location = request.form['location']
            pic_name = secure_filename(pic.filename)
            mimetype = pic.mimetype
            date = request.form['date']
            if not pic_name or not mimetype:
                return 'bad upload',400
            print(os.path.join(Upload_Folder, pic_name))
            pic.save(os.path.join(Upload_Folder, pic_name))

            file_path = './static/pictures/'+pic_name
            product_det.filename=pic_name
            product_det.location=location
            product_det.date=date
            product_det.image=file_path
            product_det.mimetype=mimetype
            
            db.session.add(product_det)
            db.session.commit()
            product_det = Product.query.all()
            return redirect(url_for('main.list'))
    else:
            return render_template('update.html',product_det=product_det)
        
# Delete Camps Details        
@main.route('/<int:id>/delete', methods=['GET'])
def delete(id):
            product_det = Product.query.filter_by(id=id).first()
            if request.method =="GET" and product_det:
                db.session.delete(product_det)
                db.session.commit()
            return redirect(url_for('main.list'))
 
# Show Camps Details Using Action Button        
@main.route('/<int:id>/show_list', methods=['GET','POST']) 
def show_list(id):
        product_det = Product.query.filter_by(id=id).first()
        return render_template('show_list.html',product_det=product_det)
               