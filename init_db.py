from app import app, db
from model import Admin

# Create an application context
with app.app_context():
    # Create the database and tables
    db.create_all()

    # Create an admin user
    admin = Admin(username='admin')
    admin.set_password('2103')
    db.session.add(admin)
    db.session.commit()
    
    print("Database initialized successfully!")