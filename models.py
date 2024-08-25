from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
import re

# Metadata with naming conventions
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

# User Model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    orders = db.relationship('Order', back_populates='user', cascade="all, delete-orphan")

    @validates('email')
    def validate_email(self, key, email):
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email.lower()  # Making email case-insensitive

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if value and (len(value) < 10 or len(value) > 15):
            raise ValueError("Phone number must be between 10 and 15 characters")
        return value

    def __repr__(self):
        return f'<User {self.user_id}, {self.user_name}, {self.email}>'

# BeamBlock Model
class BeamBlock(db.Model, SerializerMixin):
    __tablename__ = 'beamblocks'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

    order_beamblocks = db.relationship('OrderProduct', back_populates='beamblock')

    serialize_rules = ('-order_beamblocks.beamblock',)

    def __repr__(self):
        return f'<BeamBlock id={self.id} price={self.price}>'

# HollowBlock Model
class HollowBlock(db.Model, SerializerMixin):
    __tablename__ = 'hollowblocks'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

    order_hollowblocks = db.relationship('OrderProduct', back_populates='hollowblock')

    serialize_rules = ('-order_hollowblocks.hollowblock',)

    def __repr__(self):
        return f'<HollowBlock id={self.id} price={self.price}>'

# PavingBlock Model
class PavingBlock(db.Model, SerializerMixin):
    __tablename__ = 'pavingblocks'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

    order_pavingblocks = db.relationship('OrderProduct', back_populates='pavingblock')

    serialize_rules = ('-order_pavingblocks.pavingblock',)

    def __repr__(self):
        return f'<PavingBlock id={self.id} price={self.price}>'

# RoadKerb Model
class RoadKerb(db.Model, SerializerMixin):
    __tablename__ = 'roadkerbs'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

    order_roadkerbs = db.relationship('OrderProduct', back_populates='roadkerb')

    serialize_rules = ('-order_roadkerbs.roadkerb',)

    def __repr__(self):
        return f'<RoadKerb id={self.id} price={self.price}>'

# Service Model
class Service(db.Model, SerializerMixin):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

    order_services = db.relationship('OrderProduct', back_populates='service')

    serialize_rules = ('-order_services.service',)

    def __repr__(self):
        return f'<Service id={self.id} price={self.price}>'

# Gallery Model
class Gallery(db.Model, SerializerMixin):
    __tablename__ = 'gallery'
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Gallery id={self.id}>'

# Order Model
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)

    order_products = db.relationship('OrderProduct', back_populates='order', cascade="all, delete-orphan")
    user = db.relationship('User', back_populates='orders')

    serialize_rules = ('-order_products.order', '-user.orders', '-user.password')

    def __repr__(self):
        return f'<Order id={self.id} user_id={self.user_id} order_date={self.order_date} total_price={self.total_price}>'

# OrderProduct Model
class OrderProduct(db.Model, SerializerMixin):
    __tablename__ = 'order_products'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    beamblock_id = db.Column(db.Integer, db.ForeignKey('beamblocks.id'), nullable=True)
    hollowblock_id = db.Column(db.Integer, db.ForeignKey('hollowblocks.id'), nullable=True)
    pavingblock_id = db.Column(db.Integer, db.ForeignKey('pavingblocks.id'), nullable=True)
    roadkerb_id = db.Column(db.Integer, db.ForeignKey('roadkerbs.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)

    order = db.relationship('Order', back_populates='order_products')
    beamblock = db.relationship('BeamBlock', back_populates='order_beamblocks')
    hollowblock = db.relationship('HollowBlock', back_populates='order_hollowblocks')
    pavingblock = db.relationship('PavingBlock', back_populates='order_pavingblocks')
    roadkerb = db.relationship('RoadKerb', back_populates='order_roadkerbs')
    service = db.relationship('Service', back_populates='order_services')

    serialize_rules = ('-order.order_products', '-beamblock.order_beamblocks', '-hollowblock.order_hollowblocks',
                       '-pavingblock.order_pavingblocks', '-roadkerb.order_roadkerbs', '-service.order_services')

    def __repr__(self):
        return f'<OrderProduct id={self.id} order_id={self.order_id}>'