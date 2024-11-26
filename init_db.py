import os
from dotenv import load_dotenv 
from app import app
from extensions import db
from model import User, Admin, Customer, ServiceProfessional, Service,SubService, ServiceRequest

load_dotenv()

def init_db():
    app.config.from_object('config.DevelopmentConfig')
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

        print("Created admin user")

        # Create all services
        services = [
            Service(
                name='Plumbing',
                price=79.99,
                time_required=90,
                description='Professional plumbing services including repairs, installations, and maintenance'
            ),
            Service(
                name='Cleaning',
                price=49.99,
                time_required=120,
                description='Professional cleaning services for homes and offices'
            ),
            Service(
                name='Haircut',
                price=29.99,
                time_required=45,
                description='Professional haircut services at your doorstep'
            ),
            Service(
                name='Pest Control',
                price=129.99,
                time_required=150,
                description='Complete pest control treatment for your property'
            ),
            Service(
                name='Painting',
                price=199.99,
                time_required=480,
                description='Professional painting services for interior and exterior'
            ),
            Service(
                name='Carpentry',
                price=89.99,
                time_required=180,
                description='Expert carpentry services for furniture repair and custom work'
            ),
            Service(
                name='Gardening',
                price=69.99,
                time_required=120,
                description='Professional gardening and landscaping services'
            ),
            Service(
                name='Home Renovation',
                price=299.99,
                time_required=960,
                description='Complete home renovation and remodeling services'
            ),
            Service(
                name='Electrical Work',
                price=89.99,
                time_required=120,
                description='Professional electrical repair and installation services'
            )
        ]

        for service in services:
            db.session.add(service)

            print(f"Created service: {service.name}")

        db.session.commit()
        print("Created all services")

        # Create sub services
        # After creating the main services
        plumbing = Service.query.filter_by(name='Plumbing').first()

        plumbing_sub_services = [
            SubService(
                parent_service_id=plumbing.id,
                name='Leaky Faucet Repair',
                description='Expert repair for leaky faucets',
                price=49.99,
                time_required=60
            ),
            SubService(
                parent_service_id=plumbing.id,
                name='Pipe Installation',
                description='Professional pipe installation services',
                price=149.99,
                time_required=180
            ),
            SubService(
                parent_service_id=plumbing.id,
                name='Toilet Repair',
                description='Fix toilet issues efficiently and quickly',
                price=79.99,
                time_required=90
            ),
            SubService(
                parent_service_id=plumbing.id,
                name='Drain Cleaning',
                description='Unclog drains and clean pipelines',
                price=99.99,
                time_required=120
            ),
            SubService(
                parent_service_id=plumbing.id,
                name='Water Heater Installation',
                description='Install or replace your water heater',
                price=199.99,
                time_required=240
            )
        ]

        for sub_service in plumbing_sub_services:
            db.session.add(sub_service)
        db.session.commit()

        #electricals

        electricals = Service.query.filter_by(name='Electrical Work').first()

        electrical_sub_services = [
            SubService(
                parent_service_id=electricals.id,
                name='Ceiling Fan Installation',
                description='Professional ceiling fan installation services.',
                price=49.99,
                time_required=60
            ),
            SubService(
                parent_service_id=electricals.id,
                name='Light Fixture Installation',
                description='Expert light fixture installation for your home.',
                price=149.99,
                time_required=180
            ),
            SubService(
                parent_service_id=electricals.id,
                name='Outlet Installation',
                description='Install new electrical outlets in your home.',
                price=79.99,
                time_required=90
            ),
            SubService(
                parent_service_id=electricals.id,
                name='Wiring Repair',
                description='Repair faulty wiring to ensure safety.',
                price=99.99,
                time_required=120
            ),
            SubService(
                parent_service_id=electricals.id,
                name='Surge Protection',
                description='Protect your home from electrical surges.',
                price=199.99,
                time_required=240
            )
        ]

        for sub_service in electrical_sub_services:
            db.session.add(sub_service)
        db.session.commit()


        #pest control

        pest_control = Service.query.filter_by(name='Pest Control').first()

        pest_control_sub_services = [
            SubService(
                parent_service_id=pest_control.id,
                name='Termite Control',
                description='Protect your home from termite infestations.',
                price=49.99,
                time_required=60
            ),
            SubService(
                parent_service_id=pest_control.id,
                name='Rodent Control',
                description='Eliminate rats and mice from your premises.',
                price=149.99,
                time_required=180
            ),
            SubService(
                parent_service_id=pest_control.id,
                name='Cockroach Control',
                description='Effective solutions to remove cockroaches.',
                price=79.99,
                time_required=90
            ),
            SubService(
                parent_service_id=pest_control.id,
                name='Bed Bug Treatment',
                description='Get rid of bed bugs and ensure a peaceful sleep.',
                price=99.99,
                time_required=120
            ),
            SubService(
                parent_service_id=pest_control.id,
                name='Mosquito Control',
                description='Reduce mosquito populations in your area.',
                price=199.99,
                time_required=240
            )
        ]

        for sub_service in pest_control_sub_services:
            db.session.add(sub_service)
        db.session.commit()


        # Cleaning Services
        cleaning = Service.query.filter_by(name='Cleaning').first()
        cleaning_sub_services = [
            SubService(
                parent_service_id=cleaning.id,
                name='House Deep Cleaning',
                description='Complete deep cleaning of your home',
                price=149.99,
                time_required=240
            ),
            SubService(
                parent_service_id=cleaning.id,
                name='Office Cleaning',
                description='Professional cleaning for office spaces',
                price=199.99,
                time_required=180
            ),
            SubService(
                parent_service_id=cleaning.id,
                name='Carpet Cleaning',
                description='Deep carpet cleaning and sanitization',
                price=89.99,
                time_required=120
            ),
            SubService(
                parent_service_id=cleaning.id,
                name='Window Cleaning',
                description='Professional window and glass cleaning',
                price=69.99,
                time_required=90
            ),
            SubService(
                parent_service_id=cleaning.id,
                name='Bathroom Deep Cleaning',
                description='Thorough bathroom cleaning and sanitization',
                price=79.99,
                time_required=120
            )
        ]
        for sub_service in cleaning_sub_services:
            db.session.add(sub_service)
        db.session.commit()

        # Painting Services
        painting = Service.query.filter_by(name='Painting').first()
        painting_sub_services = [
            SubService(
                parent_service_id=painting.id,
                name='Interior Wall Painting',
                description='Professional interior wall painting',
                price=299.99,
                time_required=480
            ),
            SubService(
                parent_service_id=painting.id,
                name='Exterior House Painting',
                description='Complete exterior house painting',
                price=499.99,
                time_required=720
            ),
            SubService(
                parent_service_id=painting.id,
                name='Furniture Painting',
                description='Refresh your furniture with professional painting',
                price=149.99,
                time_required=240
            ),
            SubService(
                parent_service_id=painting.id,
                name='Door and Window Painting',
                description='Paint doors and windows with precision',
                price=99.99,
                time_required=180
            ),
            SubService(
                parent_service_id=painting.id,
                name='Decorative Painting',
                description='Custom decorative painting and designs',
                price=199.99,
                time_required=360
            )
        ]
        for sub_service in painting_sub_services:
            db.session.add(sub_service)
        db.session.commit()

        # Continue with other services...

        # Gardening Services
        gardening = Service.query.filter_by(name='Gardening').first()
        gardening_sub_services = [
            SubService(
                parent_service_id=gardening.id,
                name='Lawn Mowing',
                description='Professional lawn mowing services',
                price=49.99,
                time_required=60
            ),
            SubService(
                parent_service_id=gardening.id,
                name='Garden Maintenance',
                description='Regular maintenance for your garden',
                price=89.99,
                time_required=120
            ),
            SubService(
                parent_service_id=gardening.id,
                name='Planting Services',
                description='Expert planting of flowers and trees',
                price=69.99,
                time_required=90
            ),
            SubService(
                parent_service_id=gardening.id,
                name='Irrigation System Installation',
                description='Install and maintain irrigation systems',
                price=149.99,
                time_required=180
            ),
            SubService(
                parent_service_id=gardening.id,
                name='Landscape Design',
                description='Custom landscape design services',
                price=199.99,
                time_required=240
            )
        ]
        for sub_service in gardening_sub_services:
            db.session.add(sub_service)
        db.session.commit()

        # Carpentry Services
        carpentry = Service.query.filter_by(name='Carpentry').first()
        carpentry_sub_services = [
            SubService(
                parent_service_id=carpentry.id,
                name='Furniture Repair',
                description='Expert furniture repair and restoration',
                price=79.99,
                time_required=120
            ),
            SubService(
                parent_service_id=carpentry.id,
                name='Custom Furniture Making',
                description='Create custom furniture pieces',
                price=299.99,
                time_required=480
            ),
            SubService(
                parent_service_id=carpentry.id,
                name='Door Installation/Repair',
                description='Professional door services',
                price=89.99,
                time_required=120
            ),
            SubService(
                parent_service_id=carpentry.id,
                name='Cabinet Making',
                description='Custom cabinet design and installation',
                price=199.99,
                time_required=360
            ),
            SubService(
                parent_service_id=carpentry.id,
                name='Wood Floor Repair',
                description='Repair and restore wooden flooring',
                price=149.99,
                time_required=240
            )
        ]
        for sub_service in carpentry_sub_services:
            db.session.add(sub_service)
        db.session.commit()

        # Haircut Services
        haircut = Service.query.filter_by(name='Haircut').first()
        haircut_sub_services = [
            SubService(
                parent_service_id=haircut.id,
                name='Men\'s Haircut',
                description='Professional men\'s haircut services',
                price=29.99,
                time_required=30
            ),
            SubService(
                parent_service_id=haircut.id,
                name='Women\'s Haircut',
                description='Expert women\'s haircut and styling',
                price=49.99,
                time_required=60
            ),
            SubService(
                parent_service_id=haircut.id,
                name='Kids Haircut',
                description='Gentle and professional kids haircuts',
                price=24.99,
                time_required=30
            ),
            SubService(
                parent_service_id=haircut.id,
                name='Hair Styling',
                description='Professional hair styling services',
                price=39.99,
                time_required=45
            ),
            SubService(
                parent_service_id=haircut.id,
                name='Hair Treatment',
                description='Deep conditioning and treatment',
                price=59.99,
                time_required=90
            )
        ]
        for sub_service in haircut_sub_services:
            db.session.add(sub_service)
        db.session.commit()

        # Home Renovation Services
        renovation = Service.query.filter_by(name='Home Renovation').first()
        renovation_sub_services = [
            SubService(
                parent_service_id=renovation.id,
                name='Kitchen Remodeling',
                description='Complete kitchen renovation and upgrades',
                price=2999.99,
                time_required=2880  # 48 hours
            ),
            SubService(
                parent_service_id=renovation.id,
                name='Bathroom Renovation',
                description='Modernize your bathroom with our renovation services',
                price=1999.99,
                time_required=1440  # 24 hours
            ),
            SubService(
                parent_service_id=renovation.id,
                name='Living Room Makeover',
                description='Transform your living space with a custom design',
                price=1499.99,
                time_required=1200
            ),
            SubService(
                parent_service_id=renovation.id,
                name='Flooring Replacement',
                description='Install new flooring for a refreshed look',
                price=999.99,
                time_required=720
            ),
            SubService(
                parent_service_id=renovation.id,
                name='Room Additions',
                description='Expand your home with expertly designed room additions',
                price=3999.99,
                time_required=4320  # 72 hours
            )
        ]
        for sub_service in renovation_sub_services:
            db.session.add(sub_service)
        db.session.commit()






     

if __name__ == '__main__':
    init_db()