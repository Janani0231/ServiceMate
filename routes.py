import os
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from model import User, Customer, ServiceProfessional, Service,SubService, ServiceRequest
from werkzeug.utils import secure_filename
from datetime import datetime
from forms import LoginForm, RegisterForm, ServiceForm,ServiceRequestForm
from app import app
from extensions import db
from sqlalchemy import or_


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/test_db')
def test_db():
    try:
        users = User.query.all()
        return f"Database connected. Found {len(users)} users."
    except Exception as e:
        return f"Database error: {str(e)}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session['user_type'] = user.type
            session['user_id'] = user.id
            flash('Logged in successfully.', 'success')
            # Use the common dashboard route instead of specific ones
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.user_type.data == 'customer':
            user = Customer(username=form.username.data, email=form.email.data, address=form.address.data, phone=form.phone.data)
        else:
            user = ServiceProfessional(username=form.username.data, email=form.email.data, name=form.name.data, description=form.description.data, service_type=form.service_type.data, experience=form.experience.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/register/professional', methods=['GET', 'POST'])
def register_professional():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(username=form.email.data).first()
            if existing_user:
                flash('Email already registered. Please use a different email.', 'danger')
                return render_template('professional/professional_register.html', form=form)

            filename = None
            if form.documents.data:
                filename = secure_filename(form.documents.data.filename)
                form.documents.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
            user = ServiceProfessional(
                username=form.email.data,
                email=form.email.data,
                name=form.name.data,
                address=form.address.data,
                pincode=form.pincode.data,
                service_type=form.service_type.data,
                experience=form.experience.data,
                documents_path=filename,
                type='service_professional'  # Make sure to set the user type
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Registration error: {str(e)}")
            flash(f'Registration failed: {str(e)}', 'danger')
            return render_template('professional/professional_register.html', form=form)
    
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
                
    return render_template('professional/professional_register.html', form=form)

@app.route('/register/customer', methods=['GET', 'POST'])
def register_customer():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(username=form.email.data).first()
            if existing_user:
                flash('Email already registered. Please use a different email.', 'danger')
                return render_template('customer/customer_register.html', form=form)

            user = Customer(
                username=form.email.data,
                email=form.email.data,
                name=form.name.data,
                address=form.address.data,
                pincode=form.pincode.data,
                type='customer'  # Make sure to set the user type
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Registration error: {str(e)}")
            flash(f'Registration failed: {str(e)}', 'danger')
            return render_template('customer/customer_register.html', form=form)
    
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
                
    return render_template('customer/customer_register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.type == 'admin':
        total_services = Service.query.count()
        active_professionals = ServiceProfessional.query.filter_by(is_approved=True).count()
        total_customers = Customer.query.count()
        
        return render_template('admin/dashboard.html',
                               total_services=total_services,
                               active_professionals=active_professionals,
                               total_customers=total_customers)
    elif current_user.type == 'customer':
        return render_template('customer/dashboard.html')
    elif current_user.type == 'service_professional':
        return render_template('professional/dashboard.html')
    


@app.route('/admin/services', methods=['GET', 'POST'])
@login_required
def manage_services():
    # Check if user is admin
    if current_user.type != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = ServiceForm()
    if form.validate_on_submit():
        try:
            service = Service(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                time_required=form.time_required.data
            )
            db.session.add(service)
            db.session.commit()
            flash('Service added successfully.', 'success')
            return redirect(url_for('manage_services'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding service: {str(e)}', 'danger')
    
    # Get all services for display
    services = Service.query.all()
    return render_template('admin/services.html', services=services, form=form)

@app.route('/admin/services/delete/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    if current_user.type != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    service = Service.query.get_or_404(service_id)
    try:
        db.session.delete(service)
        db.session.commit()
        flash('Service deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting service: {str(e)}', 'danger')
    
    return redirect(url_for('manage_services'))

@app.route('/debug/services')
def debug_services():
    try:
        services = Service.query.all()
        service_data = []
        for service in services:
            service_data.append({
                'id': service.id,
                'name': service.name,
                'price': service.price,
                'time_required': service.time_required,
                'is_active': service.is_active
            })
        return {'services': service_data}
    except Exception as e:
        return {'error': str(e)}


@app.route('/admin/services/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    if current_user.type != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    service = Service.query.get_or_404(service_id)
    form = ServiceForm(obj=service)
    
    if form.validate_on_submit():
        try:
            service.name = form.name.data
            service.description = form.description.data
            service.price = form.price.data
            service.time_required = form.time_required.data
            db.session.commit()
            flash('Service updated successfully.', 'success')
            return redirect(url_for('manage_services'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating service: {str(e)}', 'danger')
    
    return render_template('admin/edit_service.html', form=form, service=service)

#for second table of admin dashboard professionals management 
@app.route('/admin/professionals')
@login_required
def manage_professionals():
    if current_user.type != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    professionals = ServiceProfessional.query.all()
    return render_template('admin/professionals.html', professionals=professionals)

@app.route('/admin/professionals/<int:professional_id>/<action>')
@login_required
def manage_professional_status(professional_id, action):
    if current_user.type != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    professional = ServiceProfessional.query.get_or_404(professional_id)
    
    try:
        if action == 'approve':
            professional.is_approved = True
            flash('Professional approved successfully.', 'success')
        elif action == 'reject':
            professional.is_approved = False
            flash('Professional rejected.', 'success')
        elif action == 'delete':
            db.session.delete(professional)
            flash('Professional deleted successfully.', 'success')
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating professional status: {str(e)}', 'danger')
    
    return redirect(url_for('manage_professionals'))

@app.route('/admin/service-requests')
@login_required
def manage_service_requests():
    if current_user.type != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get all service requests with status filter
    status_filter = request.args.get('status', 'all')
    if status_filter == 'all':
        requests = ServiceRequest.query.all()
    else:
        requests = ServiceRequest.query.filter_by(status=status_filter).all()
    
    return render_template('admin/service_requests.html', requests=requests, current_filter=status_filter)    

@app.route('/admin/search')
@login_required
def admin_search():
    if current_user.type != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'service_request')
    
    results = []
    if query:
        if search_type == 'service_request':
            results = ServiceRequest.query.filter(
                or_(ServiceRequest.id.contains(query),
                ServiceRequest.status.contains(query)
                )
            ).all()
        elif search_type == 'professional':
            results = ServiceProfessional.query.filter(
                or_(ServiceProfessional.id.contains(query),
                ServiceProfessional.name.contains(query)
                )
            ).all()
        elif search_type == 'customer':
            results = Customer.query.filter(
                or_(Customer.id.contains(query),
                Customer.name.contains(query)
                )
            ).all()
        elif search_type == 'services':
            results = Service.query.filter(
                or_(Service.id.contains(query),
                Service.name.contains(query)
                )
            ).all()
    
    return render_template('admin/search.html', results=results, query=query, search_type=search_type)

@app.route('/service/<int:service_id>/request', methods=['GET', 'POST'])
@login_required
def create_service_request(service_id):
    if current_user.type != 'customer':
        flash('Only customers can create service requests.', 'error')
        return redirect(url_for('index'))
        
    sub_service = SubService.query.get_or_404(service_id)
    form = ServiceRequestForm()
    
    if form.validate_on_submit():
        request = ServiceRequest(
            service_id=sub_service.parent_service_id,  # Link to parent service
            sub_service_id=sub_service.id,  # Add this field to ServiceRequest model
            customer_id=current_user.id,
            preferred_date=form.preferred_date.data,
            preferred_time=form.preferred_time.data,
            address=form.address.data,
            pincode=form.pincode.data,
            description=form.description.data,
            status='requested'
        )
        db.session.add(request)
        db.session.commit()
        
        flash('Service request submitted successfully!', 'success')
        return redirect(url_for('customer_dashboard'))
        
    return render_template('customer/create_request.html', 
                         form=form, 
                         service=sub_service.parent_service,
                         sub_service=sub_service)

@app.route('/professional/requests')
@login_required
def professional_requests():
    if current_user.type != 'service_professional':
        return redirect(url_for('index'))
        
    pending_requests = ServiceRequest.query.filter(
        ServiceRequest.status == 'requested',
        ServiceRequest.service_id == current_user.service_type
    ).all()
    
    my_requests = ServiceRequest.query.filter(
        ServiceRequest.professional_id == current_user.id
    ).all()
    
    return render_template('professional/requests.html', 
                         pending_requests=pending_requests,
                         my_requests=my_requests)

@app.route('/request/<int:request_id>/<action>')
@login_required
def handle_request(request_id, action):
    if current_user.type != 'service_professional':
        return redirect(url_for('index'))
        
    request = ServiceRequest.query.get_or_404(request_id)
    
    if action == 'accept':
        request.professional_id = current_user.id
        request.status = 'accepted'
        flash('Request accepted successfully!', 'success')
    elif action == 'complete':
        request.status = 'completed'
        request.date_of_completion = datetime.utcnow()
        flash('Request marked as completed!', 'success')
    
    db.session.commit()
    return redirect(url_for('professional_requests'))

@app.route('/customer/dashboard')
@login_required
def customer_dashboard():
    if current_user.type != 'customer':
        return redirect(url_for('index'))
        
    active_requests = ServiceRequest.query.filter(
        ServiceRequest.customer_id == current_user.id,
        ServiceRequest.status.in_(['requested', 'accepted'])
    ).all()
    
    completed_requests = ServiceRequest.query.filter(
        ServiceRequest.customer_id == current_user.id,
        ServiceRequest.status == 'completed'
    ).all()
    
    return render_template('customer/dashboard.html',
                         active_requests=active_requests,
                         completed_requests=completed_requests)


"""
@app.route('/book_service/<service_id>', methods=['GET', 'POST'])
@login_required
def book_service(service_id):
    # Fetch the service details using the service_id
    service = Service.query.filter_by(id=service_id).first_or_404()
    
    # Logic for booking the service
    if request.method == 'POST':
        # Handle the booking logic here
        # For example, create a new ServiceRequest
        service_request = ServiceRequest(
            service_id=service.id,
            customer_id=current_user.id,
            status='requested'
        )
        db.session.add(service_request)
        db.session.commit()
        flash('Service booked successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('book_service.html', service=service)"""

    
"""@app.route('/products')
@login_required
def products():
    return render_template('customer/products.html')

from flask import render_template
from flask_login import login_required

@app.route('/products')
@login_required
def products():
    return render_template('customer/products.html')"""


#second comment

"""@app.route('/customer/products/plumbing')
@login_required
def plumbing_products():
    plumbing_service = Service.query.filter_by(name='Plumbing').first()
    if not plumbing_service:
        flash('Service not found', 'error')
        return redirect(url_for('customer_dashboard'))
        
    sub_services = SubService.query.filter_by(
        parent_service_id=plumbing_service.id,
        is_active=True
    ).all()
    
    return render_template('customer/products/plumbing.html', sub_services=sub_services)

@app.route('/customer/products/cleaning')
@login_required
def cleaning_products():
    cleaning_service = Service.query.filter_by(name='Cleaning').first()
    if not cleaning_service:
        flash('Service not found', 'error')
        return redirect(url_for('customer_dashboard'))
        
    sub_services = SubService.query.filter_by(
        parent_service_id=cleaning_service.id,
        is_active=True
    ).all()
    
    return render_template('customer/products/cleaning.html', sub_services=sub_services)

@app.route('/customer/products/haircut')
@login_required
def haircut_products():
    return render_template('customer/products/haircut.html')

@app.route('/customer/products/pest_control')
@login_required
def pest_control_products():
    pest_control_service = Service.query.filter_by(name='Pest Control').first()
    if not pest_control_service:
        flash('Service not found', 'error')
        return redirect(url_for('customer_dashboard'))
        
    sub_services = SubService.query.filter_by(
        parent_service_id=pest_control_service.id,
        is_active=True
    ).all()
    
    return render_template('customer/products/pest_control.html', sub_services=sub_services)

@app.route('/customer/products/painting')
@login_required
def painting_products():
    return render_template('customer/products/painting.html')

@app.route('/customer/products/carpentry')
@login_required
def carpentry_products():
    return render_template('customer/products/carpentry.html')

@app.route('/customer/products/gardening')
@login_required
def gardening_products():
    return render_template('customer/products/gardening.html')

@app.route('/customer/products/home_renovation')
@login_required
def home_renovation_products():
    return render_template('customer/products/home_renovation.html')

@app.route('/customer/products/electricals')
@login_required
def electrical_products():
    electrical_service = Service.query.filter_by(name='Electrical Work').first()
    if not electrical_service:
        flash('Service not found', 'error')
        return redirect(url_for('customer_dashboard'))
        
    sub_services = SubService.query.filter_by(
        parent_service_id=electrical_service.id,
        is_active=True
    ).all()
    
    return render_template('customer/products/electricals.html', sub_services=sub_services)"""

@app.route('/customer/products/<service_type>')
@login_required
def service_products(service_type):
    service = Service.query.filter_by(name=service_type.replace('_', ' ').title()).first()
    if not service:
        flash('Service not found', 'error')
        return redirect(url_for('customer_dashboard'))
        
    sub_services = SubService.query.filter_by(
        parent_service_id=service.id,
        is_active=True
    ).all()
    
    template_name = f'customer/products/{service_type}.html'
    return render_template(template_name, sub_services=sub_services, service=service)