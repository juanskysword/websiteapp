from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, product, order_product
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/shop')
def shop():
    product_list = product.query.all()
    for product_i in product_list:
            price = str(product_i.price)  
            price = f'${price[:-2]}.{price[-2:]}'
            product_i.price = price
             
    return render_template('shop.html', user=current_user, product_list=product_list)


# @views.route('/product')
# def addcart():
#     order_products = order_product.query.all()
#     for products_i in order_products:
#             order = str(products_i.order)
#             order = f'${order[:-2]}.{order[-2:]}'
#             products_i.order = order
    
#     return render_template('product.html', user=current_user, order_products=order_products)