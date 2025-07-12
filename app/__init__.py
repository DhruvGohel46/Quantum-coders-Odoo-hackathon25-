from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Set up login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes.main_routes import main
    from app.routes.auth_routes import auth
    from app.routes.admin_routes import admin
    from app.routes.item_routes import items
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(items)
    
    return app
