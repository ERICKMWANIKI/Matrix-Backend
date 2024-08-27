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
        db.session.commit()  # Make sure to commit the deletions

def seed_data():
    with app.app_context():
        try:
            print("Creating users...")
            user1 = User(user_name="John Doe", email="john@example.com", password="password", role="customer", phone_number="1234567890")
            user2 = User(user_name="Jane Smith", email="jane@example.com", password="password", role="customer", phone_number="0987654321")
            admin = User(user_name="Admin User", email="admin@example.com", password="password", role="admin", phone_number="1122334455")
            users = [user1, user2, admin]

            print("Creating beamblocks...")
            beamblock1 = BeamBlock(price=13.50, image_url='/static/BeamBlockSystem 1.jpeg', description='High-quality beam block')
            beamblock2 = BeamBlock(price=15.75, image_url='/static/BeamBlock 2.jpeg', description='Durable beam block')
            beamblock3 = BeamBlock(price=10.50, image_url='/static/BeamBlock 3.jpeg', description='High-quality beam block')
            beamblock4 = BeamBlock(price=15.75, image_url='/static/BeamBlock 4.jpeg', description='Durable beam block')
            beamblock5 = BeamBlock(price=14.50, image_url='/static/BeamBlock 5.jpeg', description='Good quality beam block')
            beamblocks = [beamblock1, beamblock2, beamblock3, beamblock4, beamblock5]

            print("Creating hollowblocks...")
            hollowblock1 = HollowBlock(price=8.25, image_url='/static/HollowBlock 1.jpeg', description='Strong hollow block')
            hollowblock2 = HollowBlock(price=12.00, image_url='/static/HollowBlock 2.jpeg', description='Reliable hollow block')
            hollowblock3 = HollowBlock(price=8.25, image_url='/static/HollowBlock 3.jpeg', description='Strong hollow block')
            hollowblock4 = HollowBlock(price=12.00, image_url='/static/HollowBlock 4.jpeg', description='Reliable hollow block')
            hollowblock5 = HollowBlock(price=8.25, image_url='/static/HollowBlock 5.jpeg', description='Strong hollow block')
            
            hollowblocks = [hollowblock1, hollowblock2, hollowblock3, hollowblock4, hollowblock5]

            print("Creating pavingblocks...")
            pavingblock1 = PavingBlock(price=5.75, image_url='/static/PavingBlock 1.jpeg', description='Smooth paving block')
            pavingblock2 = PavingBlock(price=7.50, image_url='/static/PavingBlock 2.jpeg', description='Textured paving block')
            pavingblock3 = PavingBlock(price=5.75, image_url='/static/PavingBlock 3.jpeg', description='Smooth paving block')
            pavingblock4 = PavingBlock(price=5.75, image_url='/static/PavingBlock 4.jpeg', description='Smooth paving block')
            pavingblock5 = PavingBlock(price=5.75, image_url='/static/PavingBlock 5.jpeg', description='Smooth paving block')
            pavingblocks = [pavingblock1, pavingblock2, pavingblock3, pavingblock4, pavingblock5]

            print("Creating roadkerbs...")
            roadkerb1 = RoadKerb(price=20.00, image_url='/static/RoadKerbAccessories 1.jpeg', description='Durable road kerb')
            roadkerb2 = RoadKerb(price=25.00, image_url='/static/RoadKerbAccessories 2.jpeg', description='Premium road kerb')
            roadkerb3 = RoadKerb(price=100.00, image_url='/static/RoadKerbAccessories 3.jpeg', description='Construction service')
            roadkerb4 = RoadKerb(price=100.00, image_url='/static/RoadKerbAccessories 4.jpeg', description='Construction service')
            roadkerb5 = RoadKerb(price=100.00, image_url='/static/RoadKerbAccessories 5.jpeg', description='Construction service')
            roadkerb6 = RoadKerb(price=100.00, image_url='/static/RoadKerbAccessories 6.jpeg', description='Construction service')
            roadkerb7 = RoadKerb(price=100.00, image_url='/static/RoadKerbAccessories 7.jpeg', description='Construction service')
            roadkerb8 = RoadKerb(price=100.00, image_url='/static/RoadKerbAccessories 8.jpeg', description='Construction service')
            roadkerb9 = RoadKerb(price=100.00, image_url='/static/RoadKerbAccessories 9.jpeg', description='Construction service')
            roadkerbs = [roadkerb1, roadkerb2, roadkerb3, roadkerb4, roadkerb5, roadkerb6, roadkerb7, roadkerb8, roadkerb9]

            print("Creating services...")
            service1 = Service(price=100.00, image_url='/static/Services 1.jpeg', description='Construction service')
            service2 = Service(price=150.00, image_url='/static/Services 2.jpeg', description='Landscaping service')
            service3 = Service(price=100.00, image_url='/static/Services 3.jpeg', description='Construction service')
            service4 = Service(price=100.00, image_url='/static/Services 4.jpeg', description='Construction service')
            services = [service1, service2, service3, service4]

            print("Creating gallery items...")
            gallery1 = Gallery(image_url='/static/Gallery 1.jpeg')
            gallery2 = Gallery(image_url='/static/Gallery 2.jpeg')
            gallery3 = Gallery(image_url='/static/Gallery 3.jpeg')
            gallery4 = Gallery(image_url='/static/Gallery 4.jpeg')
            gallery5 = Gallery(image_url='/static/Gallery 5.jpeg')
            gallery6 = Gallery(image_url='/static/Gallery 6.jpeg')
            gallery7 = Gallery(image_url='/static/Gallery 7.jpeg')
            gallery8 = Gallery(image_url='/static/Gallery8.jpeg')
            gallery9 = Gallery(image_url='/static/Galllery 9.jpeg')
            gallery10 = Gallery(image_url='/static/Gallery 11.jpeg')
            gallery11 = Gallery(image_url='/static/Gallery 12.jpeg')
            gallery12 = Gallery(image_url='/static/Gallery 13.jpeg')
            gallery13 = Gallery(image_url='/static/Gallery 15.jpeg')
            gallery14 = Gallery(image_url='/static/Gallery 16.jpeg')
            gallery15 = Gallery(image_url='/static/Gallery 17.jpeg')
            gallery16 = Gallery(image_url='/static/Gallery 18.jpeg')
            gallery17 = Gallery(image_url='/static/Gallery 19.jpeg')
            gallery18 = Gallery(image_url='/static/Gallery 20.jpeg')
            gallery19 = Gallery(image_url='/static/Gallery 21.jpeg')
            gallery20 = Gallery(image_url='/static/Gallery 22.jpeg')
            gallery21 = Gallery(image_url='/static/Gallery 23.jpeg')
            gallery22 = Gallery(image_url='/static/Gallery 24.jpeg')
            gallery23 = Gallery(image_url='/static/Gallery 25.jpeg')
            gallery24 = Gallery(image_url='/static/Gallery 26.jpeg')
            gallery25 = Gallery(image_url='/static/Gallery 27.jpeg')
            gallery26 = Gallery(image_url='/static/Gallery 28.jpeg')
            gallery27 = Gallery(image_url='/static/Gallery 29.jpeg')
            gallery28 = Gallery(image_url='/static/Gallery 30.jpeg')
            galleries = [gallery1, gallery2, gallery3, gallery4, gallery5, gallery6, gallery7, gallery8, gallery9, gallery10, gallery11, gallery12, gallery13, gallery14, gallery15, gallery16, gallery17, gallery18, gallery19, gallery20, gallery21, gallery22, gallery23, gallery24, gallery25, gallery26, gallery27, gallery28,]

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
    delete_data()  # This will ensure existing data is removed before seeding new data
    seed_data()
