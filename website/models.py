from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Boolean, default=False, nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(64))
    address = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zipcode = db.Column(db.String(15))
    phone_number = db.Column(db.String(15))
    notes = db.relationship('Note')

class order(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    quantity= db.Column(db.Integer)
    order_date = db.Column(db.DateTime(timezone=True), default=func.now()) 
    delivery_date = db.Column(db.String(255), nullable=True) 
    customer = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin = db.Column(db.Integer, db.ForeignKey('user.id'))

class product(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Integer)
    img = db.Column(db.String(1000)) 


class order_product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    order = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_note = db.Column(db.String(255))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
