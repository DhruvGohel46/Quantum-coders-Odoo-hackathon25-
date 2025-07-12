import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/rewear.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
