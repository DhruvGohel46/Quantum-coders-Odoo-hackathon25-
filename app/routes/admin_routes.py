from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def admin_home():
    return 'Admin route works!'
