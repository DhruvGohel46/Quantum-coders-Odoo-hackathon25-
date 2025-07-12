from flask import Blueprint

items = Blueprint('items', __name__)

@items.route('/items')
def items_home():
    return 'Items route works!'
