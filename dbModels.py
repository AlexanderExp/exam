from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Numeric

db = SQLAlchemy()


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    address = db.Column(db.String)
    rating = Column(Numeric(precision=4, scale=2))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'rating': self.rating,
        }


class MenuDish(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    dish_name = db.Column(db.String)
    price = db.Column(db.Double)
    dish_description = db.Column(db.String)

    def serialize(self):
        return {
            'id': self.id,
            'price': self.price,
            'dish_name': self.dish_name,
        }


class OrderKol(db.Model):
    __tablename__ = 'order_kol'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dish_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,

        }
