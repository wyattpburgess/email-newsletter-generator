from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from newsletter_app import db, bcrypt
from newsletter_app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm, \
    RequestResetForm
from newsletter_app.users.utils import send_reset_email
from newsletter_app.models import User

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.homepage'))
        else:
            flash('Login Failed. Please check email and password', 'alert-danger')
    title = 'Login'
    return render_template('users/login.html', title=title, form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'alert-success')
        return redirect(url_for('users.login'))
    title = 'Create a New Account'
    return render_template('users/register.html', title=title, h1=title, form=form)


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated', 'alert-success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    title = 'Manage Account - ' + current_user.username
    return render_template('users/account.html', title=title, h1=title, form=form)


@users.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction for resetting your password', 'alert-info')
        return redirect(url_for('users.login'))
    title = 'Reset Password'
    return render_template('users/reset_request.html', title=title, form=form)


@users.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token.', 'alert-error')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'alert-success')
        return redirect(url_for('users.login'))
    title = 'Reset Password'
    return render_template('users/reset_token.html', title=title, form=form)
