from app import app
from models import db, User, BeamBlock, HollowBlock, PavingBlock, RoadKerb, Service, Gallery, Order, OrderProduct
from datetime import date

def delete_data():
    with app.app_context():
        print("Deleting data...")
        OrderProduct.query.delete()
        Order.query.delete()
        Gallery.query.delete()
        Service.query.delete()
        RoadKerb.query.delete()
        PavingBlock.query.delete()
        HollowBlock.query.delete()
        BeamBlock.query.delete()
        User.query.delete()

def seed_data():
    with app.app_context():
        try:
            print("Creating users...")
            user1 = User(user_name="John Doe", email="john@example.com", password="password", role="customer", phone_number="1234567890")
            user2 = User(user_name="Jane Smith", email="jane@example.com", password="password", role="customer", phone_number="0987654321")
            admin = User(user_name="Admin User", email="admin@example.com", password="password", role="admin", phone_number="1122334455")
            users = [user1, user2, admin]

            print("Creating beamblocks...")
            beamblock1 = BeamBlock(price=10.50, image_url='static/BeamBlock.jpeg', description='High-quality beam block')
            beamblock2 = BeamBlock(price=15.75, image_url='/static/BeamBlock.jpeg', description='Durable beam block')
            beamblocks = [beamblock1, beamblock2]

            print("Creating hollowblocks...")
            hollowblock1 = HollowBlock(price=8.25, image_url='https://example.com/image3.jpg', description='Strong hollow block')
            hollowblock2 = HollowBlock(price=12.00, image_url='https://example.com/image4.jpg', description='Reliable hollow block')
            hollowblocks = [hollowblock1, hollowblock2]

            print("Creating pavingblocks...")
            pavingblock1 = PavingBlock(price=5.75, image_url='https://example.com/image5.jpg', description='Smooth paving block')
            pavingblock2 = PavingBlock(price=7.50, image_url='https://example.com/image6.jpg', description='Textured paving block')
            pavingblocks = [pavingblock1, pavingblock2]

            print("Creating roadkerbs...")
            roadkerb1 = RoadKerb(price=20.00, image_url='https://example.com/image7.jpg', description='Durable road kerb')
            roadkerb2 = RoadKerb(price=25.00, image_url='https://example.com/image8.jpg', description='Premium road kerb')
            roadkerbs = [roadkerb1, roadkerb2]

            print("Creating services...")
            service1 = Service(price=100.00, image_url='https://example.com/image9.jpg', description='Construction service')
            service2 = Service(price=150.00, image_url='https://example.com/image10.jpg', description='Landscaping service')
            services = [service1, service2]

            print("Creating gallery items...")
            gallery1 = Gallery(image_url='https://example.com/gallery1.jpg')
            gallery2 = Gallery(image_url='https://example.com/gallery2.jpg')
            galleries = [gallery1, gallery2]

            print("Creating orders...")
            order1 = Order(user=user1, total_price=250.00)
            order2 = Order(user=user2, total_price=350.00)
            orders = [order1, order2]

            print("Creating order products...")
            order_product1 = OrderProduct(order=order1, beamblock=beamblock1, hollowblock=hollowblock1)
            order_product2 = OrderProduct(order=order2, pavingblock=pavingblock1, roadkerb=roadkerb1, service=service1)
            order_products = [order_product1, order_product2]

            print("Committing to database...")
            db.session.add_all(users + beamblocks + hollowblocks + pavingblocks + roadkerbs + services + galleries + orders + order_products)
            db.session.commit()

            print("Seeding completed successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding data: {e}")

if __name__ == '__main__':
    delete_data()  # Uncomment this line if you want to delete all data before seeding
    seed_data()
