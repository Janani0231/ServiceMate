from flask import render_template, redirect, url_for, request, flash, session, current_app
from app import app
from model import db, User,Customer, ServiceProfessional, Service, ServiceRequest
from functools import wraps

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please login first.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Customer authentication decorator
def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('customer_logged_in'):
            flash('Please log in as a customer.', 'error')
            return redirect(url_for('customer_login'))
        return f(*args, **kwargs)
    return decorated_function

# Professional authentication decorator
def professional_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('professional_logged_in'):
            flash('Please log in as a professional.', 'error')
            return redirect(url_for('professional_login'))
        return f(*args, **kwargs)
    return decorated_function
