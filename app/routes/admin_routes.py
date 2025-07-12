from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def admin_home():
    return 'Admin route works!'
# app/routes/admin_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Item, User, SwapRequest
from app import db
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/panel')
@login_required
@admin_required
def panel():
    pending_items = Item.query.filter_by(is_approved=False).all()
    total_users = User.query.count()
    total_items = Item.query.count()
    pending_swaps = SwapRequest.query.filter_by(status='pending').count()
    
    return render_template('admin_panel.html', 
                         pending_items=pending_items,
                         total_users=total_users,
                         total_items=total_items,
                         pending_swaps=pending_swaps)

@admin.route('/approve_item/<int:item_id>')
@login_required
@admin_required
def approve_item(item_id):
    item = Item.query.get_or_404(item_id)
    item.is_approved = True
    db.session.commit()
    flash(f'Item "{item.title}" approved successfully!', 'success')
    return redirect(url_for('admin.panel'))

@admin.route('/reject_item/<int:item_id>')
@login_required
@admin_required
def reject_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'Item "{item.title}" rejected and removed.', 'info')
    return redirect(url_for('admin.panel'))

@admin.route('/remove_item/<int:item_id>')
@login_required
@admin_required
def remove_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'Item "{item.title}" removed successfully!', 'success')
    return redirect(url_for('admin.panel'))