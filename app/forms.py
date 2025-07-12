# app/forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, IntegerField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    category = SelectField('Category', choices=[
        ('clothing', 'Clothing'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
        ('bags', 'Bags'),
        ('jewelry', 'Jewelry')
    ], validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired(), Length(max=50)])
    size = SelectField('Size', choices=[
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('One Size', 'One Size')
    ], validators=[DataRequired()])
    condition = SelectField('Condition', choices=[
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair')
    ], validators=[DataRequired()])
    tags = StringField('Tags (comma-separated)', validators=[Length(max=200)])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    points_value = IntegerField('Points Value', validators=[NumberRange(min=1, max=100)], default=10)
    submit = SubmitField('Add Item')

class SwapRequestForm(FlaskForm):
    message = TextAreaField('Message', validators=[Length(max=500)])
    points_offered = IntegerField('Points Offered', validators=[NumberRange(min=0)], default=0)
    offered_item_id = HiddenField('Offered Item ID')
    submit = SubmitField('Send Swap Request')