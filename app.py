from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from dotenv import load_dotenv
import os
from flask_restful import Api, Resource
from models import db, User, BeamBlock, HollowBlock, PavingBlock, RoadKerb, Service, Gallery, Order, OrderProduct

# Load environment variables
load_dotenv()

# Initialize the flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY', 'super-secret')
app.json.compact = False
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db.init_app(app)

api = Api(app)

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        return response

# Decorator for Admin Access
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        if user.role != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

# Index Route
class Index(Resource):
    def get(self):
        response_dict = {"message": "Welcome to the Matrix RESTful API"}
        return make_response(jsonify(response_dict), 200)

api.add_resource(Index, '/')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.user_id)
        response = {
            "access_token": access_token,
            "role": user.role,
            "id": user.user_id
        }
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify({"error": "Invalid credentials"}), 401)

@app.route('/create_admin', methods=['POST'])
def create_admin():
    if not request.json.get('admin_key') == 'YOUR_SECRET_KEY':
        return jsonify({"error": "Unauthorized"}), 403

    username = request.json.get('username')
    password = request.json.get('password')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Hash the password
    new_admin = User(username=username, password=hashed_password, role='admin')
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": "Admin created successfully"}), 201

# Users Resource
class Users(Resource):
    def get(self):
        users = User.query.all()
        response = [user.to_dict() for user in users]
        return make_response(jsonify(response), 200)

    def post(self):
        data = request.get_json()
        email = data['email']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return make_response(jsonify({"error": "Email already exists"}), 422)

        new_user = User(
            user_name=data['user_name'],
            email=email,
            password=bcrypt.generate_password_hash(data.get("password")).decode('utf-8'),
            role=data.get('role', 'customer'),
            phone_number=data['phone_number']
        )
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.user_id)

        response = {
            "user": new_user.to_dict(),
            "access_token": access_token
        }

        return make_response(jsonify(response), 201)

api.add_resource(Users, '/users')

# UserByID Resource
class UserByID(Resource):
    @jwt_required()
    def get(self, user_id):
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        if user_id != current_user_id and User.query.get(current_user_id).role != 'admin':
            return make_response(jsonify({"error": "Access denied"}), 403)
        return make_response(jsonify(user.to_dict()), 200)

    @jwt_required()
    def patch(self, user_id):
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        if user_id != current_user_id and User.query.get(current_user_id).role != 'admin':
            return make_response(jsonify({"error": "Access denied"}), 403)
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return make_response(jsonify(user.to_dict()), 200)

    @jwt_required()
    def delete(self, user_id):
        current_user_id = get_jwt_identity()
        if User.query.get(current_user_id).role != 'admin':
            return make_response(jsonify({"error": "Admin access required"}), 403)
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message": "User deleted"}), 200)

api.add_resource(UserByID, '/users/<int:user_id>')

# BeamBlock Resource
class BeamBlocks(Resource):
    def get(self):
        beamblocks = BeamBlock.query.all()
        response = [beamblock.to_dict() for beamblock in beamblocks]
        return make_response(jsonify(response), 200)

    @admin_required
    def post(self):
        data = request.get_json()
        new_beamblock = BeamBlock(
            price=data['price'],
            image_url=data.get('image_url'),
            description=data.get('description')
        )
        db.session.add(new_beamblock)
        db.session.commit()
        return make_response(jsonify(new_beamblock.to_dict()), 201)

    @admin_required
    def delete(self):
        data = request.get_json()
        beamblock_id = data.get('beamblock_id')
        beamblock = BeamBlock.query.get_or_404(beamblock_id)
        db.session.delete(beamblock)
        db.session.commit()
        return make_response(jsonify({"message": "BeamBlock deleted"}), 200)

api.add_resource(BeamBlocks, '/beamblocks')

# HollowBlock Resource
class HollowBlocks(Resource):
    def get(self):
        hollowblocks = HollowBlock.query.all()
        response = [hollowblock.to_dict() for hollowblock in hollowblocks]
        return make_response(jsonify(response), 200)

    @admin_required
    def post(self):
        data = request.get_json()
        new_hollowblock = HollowBlock(
            price=data['price'],
            image_url=data.get('image_url'),
            description=data.get('description')
        )
        db.session.add(new_hollowblock)
        db.session.commit()
        return make_response(jsonify(new_hollowblock.to_dict()), 201)

    @admin_required
    def delete(self):
        data = request.get_json()
        hollowblock_id = data.get('hollowblock_id')
        hollowblock = HollowBlock.query.get_or_404(hollowblock_id)
        db.session.delete(hollowblock)
        db.session.commit()
        return make_response(jsonify({"message": "HollowBlock deleted"}), 200)

api.add_resource(HollowBlocks, '/hollowblocks')

# PavingBlock Resource
class PavingBlocks(Resource):
    def get(self):
        pavingblocks = PavingBlock.query.all()
        response = [pavingblock.to_dict() for pavingblock in pavingblocks]
        return make_response(jsonify(response), 200)

    @admin_required
    def post(self):
        data = request.get_json()
        new_pavingblock = PavingBlock(
            price=data['price'],
            image_url=data.get('image_url'),
            description=data.get('description')
        )
        db.session.add(new_pavingblock)
        db.session.commit()
        return make_response(jsonify(new_pavingblock.to_dict()), 201)

    @admin_required
    def delete(self):
        data = request.get_json()
        pavingblock_id = data.get('pavingblock_id')
        pavingblock = PavingBlock.query.get_or_404(pavingblock_id)
        db.session.delete(pavingblock)
        db.session.commit()
        return make_response(jsonify({"message": "PavingBlock deleted"}), 200)

api.add_resource(PavingBlocks, '/pavingblocks')

# RoadKerb Resource
class RoadKerbs(Resource):
    def get(self):
        roadkerbs = RoadKerb.query.all()
        response = [roadkerb.to_dict() for roadkerb in roadkerbs]
        return make_response(jsonify(response), 200)

    @admin_required
    def post(self):
        data = request.get_json()
        new_roadkerb = RoadKerb(
            price=data['price'],
            image_url=data.get('image_url'),
            description=data.get('description')
        )
        db.session.add(new_roadkerb)
        db.session.commit()
        return make_response(jsonify(new_roadkerb.to_dict()), 201)

    @admin_required
    def delete(self):
        data = request.get_json()
        roadkerb_id = data.get('roadkerb_id')
        roadkerb = RoadKerb.query.get_or_404(roadkerb_id)
        db.session.delete(roadkerb)
        db.session.commit()
        return make_response(jsonify({"message": "RoadKerb deleted"}), 200)

api.add_resource(RoadKerbs, '/roadkerbs')

# Service Resource
class Services(Resource):
    def get(self):
        services = Service.query.all()
        response = [service.to_dict() for service in services]
        return make_response(jsonify(response), 200)

    @admin_required
    def post(self):
        data = request.get_json()
        new_service = Service(
            price=data['price'],
            image_url=data.get('image_url'),
            description=data.get('description')
        )
        db.session.add(new_service)
        db.session.commit()
        return make_response(jsonify(new_service.to_dict()), 201)

    @admin_required
    def delete(self):
        data = request.get_json()
        service_id = data.get('service_id')
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return make_response(jsonify({"message": "Service deleted"}), 200)

api.add_resource(Services, '/services')

# Gallery Resource
class GalleryResource(Resource):
    def get(self):
        gallery = Gallery.query.all()
        response = [image.to_dict() for image in gallery]
        return make_response(jsonify(response), 200)

    @admin_required
    def post(self):
        data = request.get_json()
        new_image = Gallery(
            image_url=data.get('image_url')
        )
        db.session.add(new_image)
        db.session.commit()
        return make_response(jsonify(new_image.to_dict()), 201)

    @admin_required
    def delete(self):
        data = request.get_json()
        image_id = data.get('image_id')
        image = Gallery.query.get_or_404(image_id)
        db.session.delete(image)
        db.session.commit()
        return make_response(jsonify({"message": "Image deleted"}), 200)

api.add_resource(GalleryResource, '/gallery')

# Order Resource
class Orders(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        orders = Order.query.filter_by(user_id=current_user_id).all()
        response = [order.to_dict() for order in orders]
        return make_response(jsonify(response), 200)

    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user_id = get_jwt_identity()
        new_order = Order(
            user_id=current_user_id,
            total_price=data['total_price'],
            order_products=[
                OrderProduct(beamblock_id=product.get('beamblock_id'),
                             hollowblock_id=product.get('hollowblock_id'),
                             pavingblock_id=product.get('pavingblock_id'),
                             roadkerb_id=product.get('roadkerb_id'),
                             service_id=product.get('service_id'))
                for product in data['order_products']
            ]
        )
        db.session.add(new_order)
        db.session.commit()
        return make_response(jsonify(new_order.to_dict()), 201)

api.add_resource(Orders, '/orders')

# OrderByID Resource
class OrderByID(Resource):
    @jwt_required()
    def get(self, order_id):
        current_user_id = get_jwt_identity()
        order = Order.query.get_or_404(order_id)
        if order.user_id != current_user_id:
            return make_response(jsonify({"error": "Access denied"}), 403)
        return make_response(jsonify(order.to_dict()), 200)

api.add_resource(OrderByID, '/orders/<int:order_id>')


if __name__ == "__main__":
    app.run(port=5555, debug=True)
