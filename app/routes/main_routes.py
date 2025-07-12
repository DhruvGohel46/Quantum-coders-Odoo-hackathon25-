# app/routes/main_routes.py
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Item, SwapRequest
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    featured_items = Item.query.filter_by(is_available=True, is_approved=True).limit(6).all()
    return render_template('landing.html', featured_items=featured_items)

@main.route('/dashboard')
@login_required
def dashboard():
    user_items = Item.query.filter_by(user_id=current_user.id).all()
    pending_requests = SwapRequest.query.filter_by(owner_id=current_user.id, status='pending').count()
    sent_requests = SwapRequest.query.filter_by(requester_id=current_user.id).all()
    received_requests = SwapRequest.query.filter_by(owner_id=current_user.id).all()
    
    return render_template('dashboard.html', 
                         user_items=user_items,
                         pending_requests=pending_requests,
                         sent_requests=sent_requests,
                         received_requests=received_requests)

@main.route('/browse')
def browse():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    query = Item.query.filter_by(is_available=True, is_approved=True)
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Item.title.contains(search) | Item.description.contains(search))
    
    items = query.all()
    return render_template('browse.html', items=items, category=category, search=search)