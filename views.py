from flask import render_template, redirect, url_for, request, session, flash
from app import app
from model import Admin
from functools import wraps

# Login required decorator
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in first.')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            flash('Successfully logged in!')
            return redirect(url_for('admin_dashboard'))
        
        flash('Invalid username or password')
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
@admin_login_required
def admin_dashboard():
    admin = Admin.query.get(session['admin_id'])
    return render_template('admin/dashboard.html', admin=admin)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    flash('Successfully logged out')
    return redirect(url_for('admin_login'))