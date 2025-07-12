# app/routes/item_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models import Item, SwapRequest, User
from app.forms import ItemForm, SwapRequestForm
from app import db
from app.email_utils import send_swap_request_email
import os
from werkzeug.utils import secure_filename
import uuid

items = Blueprint('items', __name__)

@items.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            type=form.type.data,
            size=form.size.data,
            condition=form.condition.data,
            tags=form.tags.data,
            points_value=form.points_value.data,
            user_id=current_user.id
        )
        
        # Handle image upload
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            # Generate unique filename
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            form.image.data.save(filepath)
            item.image_filename = unique_filename
        
        db.session.add(item)
        db.session.commit()
        
        flash('Item added successfully! It will be available after admin approval.', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('add_item.html', form=form)

@items.route('/<int:item_id>')
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    
    # Check if user can view this item
    if not item.is_approved and item.user_id != current_user.id:
        flash('Item not found or not available.', 'error')
        return redirect(url_for('main.browse'))
    
    form = SwapRequestForm()
    user_items = []
    
    if current_user.is_authenticated and current_user.id != item.user_id:
        user_items = Item.query.filter_by(user_id=current_user.id, is_available=True).all()
    
    return render_template('item_detail.html', item=item, form=form, user_items=user_items)

@items.route('/<int:item_id>/request_swap', methods=['POST'])
@login_required
def request_swap(item_id):
    item = Item.query.get_or_404(item_id)
    
    if item.user_id == current_user.id:
        flash('You cannot swap with yourself!', 'error')
        return redirect(url_for('items.item_detail', item_id=item_id))
    
    form = SwapRequestForm()
    if form.validate_on_submit():
        swap_request = SwapRequest(
            requester_id=current_user.id,
            owner_id=item.user_id,
            item_id=item_id,
            message=form.message.data,
            points_offered=form.points_offered.data
        )
        
        if form.offered_item_id.data:
            swap_request.offered_item_id = int(form.offered_item_id.data)
        
        db.session.add(swap_request)
        db.session.commit()
        
        # Send email notification
        send_swap_request_email(item.owner, item, current_user)
        
        flash('Swap request sent successfully!', 'success')
        return redirect(url_for('items.item_detail', item_id=item_id))
    
    flash('Error sending swap request.', 'error')
    return redirect(url_for('items.item_detail', item_id=item_id))

@items.route('/swap_request/<int:request_id>/<action>')
@login_required
def handle_swap_request(request_id, action):
    swap_request = SwapRequest.query.get_or_404(request_id)
    
    if swap_request.owner_id != current_user.id:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if action == 'accept':
        swap_request.status = 'accepted'
        flash('Swap request accepted!', 'success')
    elif action == 'reject':
        swap_request.status = 'rejected'
        flash('Swap request rejected.', 'info')
    
    db.session.commit()
    return redirect(url_for('main.dashboard'))