from flask import Flask, jsonify, request

from dbModels import db, OrderKol, Restaurant, MenuDish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:liubov1969@localhost:60042/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret_key"

app.config['SESSION_COOKIE_DOMAIN'] = 'localhost'

db.init_app(app)


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    count = Restaurant.query.count()
    if count == 0:
        return jsonify({'message': 'there are no restaurants'})
    serialized_restaurants = [restaurant.serialize() for restaurant in restaurants]
    return jsonify(serialized_restaurants)


@app.route('/menu/<int:restaurant_id>', methods=['GET'])
def get_menu(restaurant_id):
    menu = MenuDish.query.filter_by(restaurant_id=restaurant_id).all()
    if len(menu) == 0:
        return jsonify({'message': "no dishes in menu in this restaurant"})
    serialized_menu = [dish.serialize() for dish in menu]
    return jsonify(serialized_menu)


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    dish_id = data.get('dish_id')
    dish = MenuDish.query.filter_by(id=dish_id).all()
    if len(dish) == 0:
        return jsonify({'message': "no such dish"})

    quantity = data.get('quantity')

    order = OrderKol(dish_id=dish_id, quantity=quantity)
    db.session.add(order)
    db.session.commit()

    return jsonify({'message': 'Order created successfully'})


@app.route('/menu/<int:restaurant_id>', methods=['POST'])
def add_dish_to_menu(restaurant_id):
    data = request.json
    dish_name = data.get('dish_name')
    price = data.get('price')
    dish_description = data.get('dish_description')
    restaurant = Restaurant.query.filter_by(id=restaurant_id).all()
    if len(restaurant) == 0:
        return jsonify({'message': 'No such restaurant'})

    dish = MenuDish(restaurant_id=restaurant_id, dish_name=dish_name, price=price, dish_description=dish_description)
    db.session.add(dish)
    db.session.commit()

    return jsonify({'message': 'Dish added to menu successfully'})


@app.route('/add_restaurants', methods=['POST'])
def add_restaurant():
    data = request.json
    name = data.get('name')
    restaurant = Restaurant.query.filter_by(name=name).all()
    if len(restaurant) > 0:
        return jsonify({'message': 'restaurant with this name already registered'})

    address = data.get('address')
    rating = data.get('rating')
    if rating < 0:
        return jsonify({'message': 'rating can not be less than 0'})

    restaurant = Restaurant(name=name, address=address, rating=rating)
    db.session.add(restaurant)
    db.session.commit()

    return jsonify({'message': 'Restaurant added successfully'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
