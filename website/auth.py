from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, order, product, order_product
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        phone_number = request.form.get('number')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')    
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(address) < 2:
            flash('Provide a real Address', category='error')  
        elif len(city) < 2:
            flash('Provide a real City', category='error')  
        elif len(state) < 2:
            flash('Provide a real State', category='error')  
        elif len(zipcode) < 2:
            flash('Provide a real Zipcode', category='error')  
        elif len(phone_number) < 2:
            flash('Provide a real Phone Number', category='error')                      
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name, address=address, city=city, state=state, zipcode= zipcode, phone_number=phone_number, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/product')
def receipt():
    User_information = User.query.all()
    Order = order_product.query.all()
    for item in Order:
        item.name = product.query.get(item.product).name
        item.price = product.query.get(item.product).price
        item.price = str(item.price)
        item.price = f'${item.price[:-2]}.{item.price[-2:]}'

    print(type(Order))
    return render_template("product.html.", user=current_user, User_information=User_information, Order = Order)
        

@auth.route('/add_to_cart/<product_id>' , methods=['POST', 'GET'])
def add_to_cart(product_id): 
    product = order_product(product=product_id, order=1, product_note='note', date= datetime.now()) 
    db.session.add(product)
    db.session.commit()
    flash('Success Item Has been Added, Proceed to checkout', category='error')
    return redirect('/shop')

# @auth.route('/createdummydata')
# def create_dummy_data():
#         product1 = product(name ='Viper CarAlarm Model 5305V', price='15099',img ='https://www.viper.com/images/products/feature/5305V.png')
#         product2 = product(name ='Prestige APS25Z', price='4999',img ='https://m.media-amazon.com/images/I/61fntOSj8dL._AC_SL1500_.jpg')
#         product3 = product(name ='DB3 Directechs', price='5999',img ='http://t1.gstatic.com/images?q=tbn:ANd9GcTmydwlA9x0yxq7mLIYr9qs-rRzV5HJUr_SwJoyOYG8dkBKYcC1')
#         db.session.add(product1)
#         db.session.add(product2)
#         db.session.add(product3)
#         db.session.commit()
#         return 'yes'

# @auth.route('/createorder')
# def create_order():
#         order_1 = order(quantity=1, order_date= datetime.now(), delivery_date ='07-20-2022', customer=1, admin=1)  
#         db.session.add(order_1)
#         db.session.commit()
#         return 'yes'

# @auth.route('/shop', methods=['GET', 'POST'])
# def shop():
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         price = request.POST.get('price')
#         img = request.POST.get('img')
#         order = order.query.filter_by(name=name).first()  
#     else:
#         new_order = order(name=name, price=price, img=img)
#         db.session.add(new_order)
#         db.session.commit()

#         return render_template("shop.html", user=current_user)

        # elif request.method == 'GET':
        #     admin_id = request.form.get('admin_id')

        #     user = User.query.filter_by(admin_id=admin_id)
        #         if admin_id(set = True)
        #         return redirect(url_for('views.home'))

