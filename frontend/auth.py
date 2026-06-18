from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
@auth_bp.route('/register.html', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_page'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Simple validations
        if not name or not email or not password or not confirm_password:
            return render_template('register.html', error="All fields are required.")
            
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', error="Email address already registered.")
            
        # Create and save user
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Log in the user and redirect to dashboard
        login_user(new_user)
        return redirect(url_for('dashboard_page'))
        
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
@auth_bp.route('/login.html', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_page'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template('login.html', error="Please enter email and password.")
            
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return render_template('login.html', error="Invalid email or password.")
            
        login_user(user)
        return redirect(url_for('dashboard_page'))
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
