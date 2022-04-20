from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, order, product, order_product

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # def create_dummy_data():
    #     product1 = product(name ='Viper CarAlarm Model 5305V', price='15099',img ='https://www.viper.com/images/products/feature/5305V.png')
    #     db.session.add(product1)
    #     db.session.commit()
    # create_dummy_data()
    return app



