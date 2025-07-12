# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    from app.routes.auth_routes import auth
    from app.routes.main_routes import main
    from app.routes.item_routes import items
    from app.routes.admin_routes import admin
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)
    app.register_blueprint(items, url_prefix='/items')
    app.register_blueprint(admin, url_prefix='/admin')
    
    return app