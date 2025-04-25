from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from src.auth.models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next')  # Retrieve the 'next' parameter from the query string
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            # Redirect to the next page if it exists, otherwise redirect to the homepage
            return redirect(next_page or url_for('fingerprint.home'))
        return render_template('auth/login.html', 
                               error_message='Invalid username or password',
                               next=next_page)
    return render_template('auth/login.html', next=next_page)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            return render_template('auth/signup.html', 
                                 error_message='Username already exists')
            
        if User.query.filter_by(email=email).first():
            return render_template('auth/signup.html', 
                                 error_message='Email already registered')
            
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('fingerprint.home'))