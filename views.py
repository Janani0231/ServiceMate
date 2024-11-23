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

# ...existing code...

"""@app.route('/')
def main_page():
    return render_template('main.html')

# ...existing code...

# Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if (username == current_app.config['ADMIN_USERNAME'] and 
            password == current_app.config['ADMIN_PASSWORD']):
            session['admin_logged_in'] = True
            flash('Welcome Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('admin/login.html')

# Customer login route
@app.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    if session.get('customer_logged_in'):
        return redirect(url_for('customer_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        customer = Customer.query.filter_by(username=username).first()
        if customer and customer.check_password(password):  # Assuming a method to verify password
            session['customer_logged_in'] = True
            session['customer_id'] = customer.id
            flash('Welcome, Customer!', 'success')
            return redirect(url_for('customer_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('customer/login.html')

# Professional login route
@app.route('/professional/login', methods=['GET', 'POST'])
def professional_login():
    if session.get('professional_logged_in'):
        return redirect(url_for('professional_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        professional = ServiceProfessional.query.filter_by(username=username).first()
        if professional and professional.check_password(password):  # Assuming a method to verify password
            session['professional_logged_in'] = True
            session['professional_id'] = professional.id
            flash('Welcome, Professional!', 'success')
            return redirect(url_for('professional_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('professional/login.html')

# Example restricted view for customers
@app.route('/customer/dashboard')
@customer_required
def customer_dashboard():
    # Fetch customer data and render customer dashboard
    return render_template('customer/dashboard.html')

# Example restricted view for professionals
@app.route('/professional/dashboard')
@professional_required
def professional_dashboard():
    # Fetch professional data and render professional dashboard
    return render_template('professional/dashboard.html')"""