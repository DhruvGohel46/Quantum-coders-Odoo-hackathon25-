# app/routes/main_routes.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Item, SwapRequest, User
from app import db

main = Blueprint('main', __name__)

def get_category_icon(category):
    mapping = {
        'clothing': 'tshirt',
        'shoes': 'shoe-sole',
        'accessories': 'handbag',
        'bags': 'handbag',
        'jewelry': 'gem',
        'outerwear': 'cloud-drizzle',
        'casual': 'tshirt',
        'formal': 'person-lines-fill',
        'default': 'box'
    }
    return mapping.get(category, 'box')

@main.route('/')
def index():
    featured_items = Item.query.filter_by(is_available=True, is_approved=True).limit(6).all()
    return render_template('landing.html', featured_items=featured_items, get_category_icon=get_category_icon)

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

@main.route('/item_details')
def item_details():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    selected_item_id = request.args.get('item', '')
    
    query = Item.query.filter_by(is_available=True, is_approved=True)
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Item.title.contains(search) | Item.description.contains(search))
    
    items = query.all()
    
    # Get selected item if specified
    selected_item = None
    similar_items = []
    if selected_item_id:
        try:
            selected_item = Item.query.get(int(selected_item_id))
            if selected_item and selected_item.is_available and selected_item.is_approved:
                # Get similar items (same category, excluding the selected item)
                similar_items = Item.query.filter(
                    Item.category == selected_item.category,
                    Item.id != selected_item.id,
                    Item.is_available == True,
                    Item.is_approved == True
                ).limit(8).all()
        except (ValueError, TypeError):
            selected_item = None
    
    return render_template('item_details.html', 
                         items=items, 
                         category=category, 
                         search=search,
                         selected_item=selected_item,
                         similar_items=similar_items,
                         get_category_icon=get_category_icon)

@main.route('/about')
def about():
    return render_template('about.html')

