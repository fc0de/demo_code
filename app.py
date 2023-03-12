import base64
import os
import faker_commerce
from random import randrange
from faker import Faker
from flask import Flask, render_template, request, redirect, url_for
from jinja2 import environment
from sqlalchemy import func
from .database import db
from .models import Customers, Products, Purchases

current_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{current_path}/app.db'
db.init_app(app)

def b64encode(s):
    return base64.b64encode(s).decode('utf8')

environment.DEFAULT_FILTERS['b64encode'] = b64encode

fake = Faker("ru_RU")
fake.add_provider(faker_commerce.Provider)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers')
@app.route('/customers/<oper>', methods=['POST'])
def customers(oper=None):
    if request.method == 'POST':
        if oper == 'add':
            person = fake.simple_profile()
            name = person['name']
            regist = fake.date_this_year()
            birth = person['birthdate']
            personal_info = fake.boolean()
            gender = person['sex']
            photo = fake.image()
            Customers.create(
                name=name,
                regist=regist,
                birth=birth,
                personal_info=personal_info,
                gender=gender,
                photo=photo
            )
        if oper == 'delete':
            user_id = request.form['user_id']
            user = Customers.get_by_id(user_id)
            user.delete()
        return redirect(url_for('customers'))

    customers = Customers.query.all()
    return render_template(
        'customers.html',
        customers=customers,
    )


@app.route('/products')
@app.route('/products/<oper>', methods=['POST'])
def products(oper=None):
    if request.method == 'POST':
        if oper == 'add':
            name = fake.ecommerce_name()
            purchase_price = randrange(10, 1000)
            sell_price = purchase_price + randrange(10, 250)
            Products.create(
                name=name,
                purchase_price=purchase_price,
                sell_price=sell_price,
            )
        if oper == 'delete':
            item_id = request.form['item_id']
            product = Products.get_by_id(item_id)
            product.delete()
        return redirect(url_for('products'))

    products = Products.query.all()
    return render_template(
        'products.html',
        products=products
    )


@app.route('/purchases')
@app.route('/purchases/<oper>', methods=['POST'])
def purchases(oper=None):
    if request.method == 'POST':
        if oper == 'add':
            customer_id = Customers.query.order_by(func.random()).first()
            product_id = Products.query.order_by(func.random()).first()
            count = randrange(1, 20)
            date = fake.date_this_month()
            Purchases.create(
                count=count,
                date=date,
                customer_id=customer_id.id,
                product_id=product_id.id,
            )
        if oper == 'delete':
            item_id = request.form['item_id']
            product = Purchases.get_by_id(item_id)
            product.delete()
        return redirect(url_for('purchases'))

    purchases = Purchases.query.all()
    return render_template(
        'purchases.html',
        purchases=purchases
    )

@app.route('/report')
def report():
    customers = Customers.query.all()
    report = [
        {
            'name': user.name,
            'sum' : user.sum_purchases()
        }
        for user in customers
    ]
    return render_template(
        'report.html',
        report=report
    )


if __name__ == "__main__":
    app.run(debug=True)