# app/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    points = db.Column(db.Integer, default=100)  # Starting points
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    items = db.relationship('Item', backref='owner', lazy=True)
    swap_requests_sent = db.relationship('SwapRequest', foreign_keys='SwapRequest.requester_id', backref='requester', lazy=True)
    swap_requests_received = db.relationship('SwapRequest', foreign_keys='SwapRequest.owner_id', backref='owner', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    condition = db.Column(db.String(20), nullable=False)
    tags = db.Column(db.String(200))
    image_filename = db.Column(db.String(100))
    points_value = db.Column(db.Integer, default=10)
    is_available = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    swap_requests = db.relationship('SwapRequest', foreign_keys='SwapRequest.item_id', backref='item', lazy=True)

class SwapRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    offered_item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True)
    points_offered = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, completed
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)