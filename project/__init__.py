from flask import Flask
from flask_login import LoginManager
from project.extensions import db

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://actecal:actecal12345@ACTECALSERVER/admindatas'
    app.config['SECRET_KEY'] = 'the random string' 
 
    from project.models import Admin,Students,Product,Important
    
    db.init_app(app) 
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.adminlogin'
    login_manager.init_app(app)
    

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Admin.query.get(int(user_id))   
    @login_manager.user_loader
    def load_user(user_id):
        return Students.query.get(int(user_id))
    @login_manager.user_loader
    def load_user(user_id):
        return Product.query.get(int(user_id))
    @login_manager.user_loader
    def load_user (user_id):
        return Important.query.get(int(user_id))
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
