import os
from dotenv import load_dotenv 
from app import app
from extensions import db
from model import User, Admin, Customer, ServiceProfessional, Service, ServiceRequest

load_dotenv()

def init_db():
    with app.app_context():
        # Drop all existing tables
        db.drop_all()

        # Create all tables
        db.create_all()

        # Create admin user
        admin_username = os.getenv('ADMIN_USERNAME')
        admin_password = os.getenv('ADMIN_PASSWORD')
        admin_email = os.getenv('ADMIN_EMAIL')
        admin = Admin(username=admin_username, email=admin_email, type='admin')
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()

        # Create sample services
        service1 = Service(name='AC Servicing', price=99.99, time_required=120, description='Professional AC maintenance and cleaning')
        service2 = Service(name='Plumbing', price=79.99, time_required=90, description='Plumbing repair and installation services')
        service3 = Service(name='Electrical Work', price=149.99, time_required=180, description='Electrical installations and troubleshooting')
        db.session.add_all([service1, service2, service3])

        # Create sample service professionals
        pro1 = ServiceProfessional(username='john_doe', email='john@example.com', type='service_professional', name='John Doe', description='Experienced AC technician', service_type='AC Servicing', experience=5, is_approved=True)
        pro1.set_password('pro1_password')
        pro2 = ServiceProfessional(username='jane_smith', email='jane@example.com', type='service_professional', name='Jane Smith', description='Skilled plumber', service_type='Plumbing', experience=8, is_approved=True)
        pro2.set_password('pro2_password')
        db.session.add_all([pro1, pro2])

        # Create sample customers
        customer1 = Customer(username='alice_cooper', email='alice@example.com', type='customer', address='123 Main St', phone='555-1234')
        customer1.set_password('customer1_password')
        customer2 = Customer(username='bob_johnson', email='bob@example.com', type='customer', address='456 Oak Rd', phone='555-5678')
        customer2.set_password('customer2_password')
        db.session.add_all([customer1, customer2])

        db.session.commit()

if __name__ == '__main__':
    init_db()