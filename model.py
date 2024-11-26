from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Admin(User):
    __tablename__ = 'admin'
    __mapper_args__ = {'polymorphic_identity': 'admin'}

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

class Customer(User):
    __tablename__ = 'customer'
    __mapper_args__ = {'polymorphic_identity': 'customer'}

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Changed to 100 to match form
    address = db.Column(db.String(200), nullable=False)  # Made nullable=False to match form requirements
    pincode = db.Column(db.String(10), nullable=False)  # Added pincode field
    phone = db.Column(db.String(20))
    requests = db.relationship('ServiceRequest', backref='customer', lazy='dynamic')
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Customer {self.name}>'

class ServiceProfessional(User):
    __tablename__ = 'service_professional'
    __mapper_args__ = {'polymorphic_identity': 'service_professional'}

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Made nullable=False
    description = db.Column(db.Text)
    service_type = db.Column(db.String(100), nullable=False)  # Made nullable=False
    experience = db.Column(db.Integer, nullable=False)  # Made nullable=False
    address = db.Column(db.String(200), nullable=False)  # Added address field
    pincode = db.Column(db.String(10), nullable=False)  # Added pincode field
    documents_path = db.Column(db.String(255))  # Added documents path
    is_approved = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    requests = db.relationship('ServiceRequest', backref='professional', lazy='dynamic')

    def __repr__(self):
        return f'<ServiceProfessional {self.name}>'

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)  # in minutes
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Service {self.name}>'

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'))
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_of_completion = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='requested')  # requested, accepted, in_progress, completed, cancelled
    remarks = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1-5 rating
    review = db.Column(db.Text)
    service = db.relationship('Service', backref='requests')
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.Time, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text)
    sub_service_id = db.Column(db.Integer, db.ForeignKey('sub_service.id'))
    sub_service = db.relationship('SubService', backref='requests')

    def __repr__(self):
        return f'<ServiceRequest {self.id}>'
    
class SubService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)  # in minutes
    is_active = db.Column(db.Boolean, default=True)
    
    parent_service = db.relationship('Service', backref='sub_services')

    def __repr__(self):
        return f'<SubService {self.name}>'