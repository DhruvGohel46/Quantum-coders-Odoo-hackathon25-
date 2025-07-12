from app import create_app, db
from app.models import Item, User

app = create_app()
app.app_context().push()

print('Database URI:', app.config.get('SQLALCHEMY_DATABASE_URI'))
print('Creating sample data...')

# Create a test user if none exists
user = User.query.filter_by(username='testuser').first()
if not user:
    user = User(username='testuser', email='test@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    print('User created:', user.username)
else:
    print('Using existing user:', user.username)

# Create an admin user if none exists
admin = User.query.filter_by(username='admin').first()
if not admin:
    admin = User(username='admin', email='admin@rewear.com', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print('Admin user created:', admin.username)
else:
    print('Using existing admin user:', admin.username)

# Create sample items
items = [
    Item(
        title='Vintage Denim Jacket',
        description='Classic vintage denim jacket in excellent condition. Perfect for casual wear or layering.',
        category='clothing',
        type='jacket',
        size='M',
        condition='excellent',
        points_value=250,
        user_id=user.id,
        is_available=True,
        is_approved=True
    ),
    Item(
        title='Nike Air Max 90',
        description='White sneakers in good condition. Comfortable and stylish.',
        category='shoes',
        type='sneakers',
        size='9',
        condition='good',
        points_value=180,
        user_id=user.id,
        is_available=True,
        is_approved=True
    ),
    Item(
        title='Leather Handbag',
        description='Brown leather handbag with gold hardware. Perfect for everyday use.',
        category='accessories',
        type='bag',
        size='One Size',
        condition='excellent',
        points_value=120,
        user_id=user.id,
        is_available=True,
        is_approved=True
    ),
    Item(
        title='Summer Dress',
        description='Floral summer dress perfect for warm weather. Light and comfortable.',
        category='clothing',
        type='dress',
        size='S',
        condition='good',
        points_value=85,
        user_id=user.id,
        is_available=True,
        is_approved=True
    ),
    Item(
        title='Vintage Leather Boots',
        description='Classic leather boots with a retro feel. Great for autumn and winter.',
        category='shoes',
        type='boots',
        size='8',
        condition='good',
        points_value=200,
        user_id=user.id,
        is_available=True,
        is_approved=True
    ),
    Item(
        title='Silk Blouse',
        description='Elegant silk blouse in navy blue. Perfect for professional settings.',
        category='clothing',
        type='blouse',
        size='M',
        condition='excellent',
        points_value=150,
        user_id=user.id,
        is_available=True,
        is_approved=True
    ),
    Item(
        title='Statement Necklace',
        description='Bold statement necklace with colorful beads. Adds personality to any outfit.',
        category='accessories',
        type='jewelry',
        size='One Size',
        condition='excellent',
        points_value=75,
        user_id=user.id,
        is_available=True,
        is_approved=True
    ),
    Item(
        title='Wool Sweater',
        description='Cozy wool sweater in forest green. Perfect for cold weather.',
        category='clothing',
        type='sweater',
        size='L',
        condition='good',
        points_value=95,
        user_id=user.id,
        is_available=True,
        is_approved=True
    )
]

# Add items to database
for item in items:
    db.session.add(item)

db.session.commit()
print('Sample items created successfully!')
print('Total items:', Item.query.count())
print('Available items:', Item.query.filter_by(is_available=True, is_approved=True).count()) 