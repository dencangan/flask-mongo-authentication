"""Routes module for authentication. This module handles all authentication/encryption related functions."""

from app import login
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user


@login.user_loader
def load_user(username):
    user = User().get_by_username(username)
    if not user:
        return None
    return User(username=user["name"])


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Main login logic."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User().get_by_username(username=login_form.username.data)
        if user is not None and User.check_password(hashed_password=user["password"], password=login_form.password.data):
            print("Password validated.")
            print(f"ID: '{user['_id']}' - Username: '{user['name']}' logging in.")
            user_obj = User(username=user["name"])
            login_user(user_obj)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            print(f"User '{login_form.username.data}' entered invalid credentials.")
            flash("Invalid username or password")

    return render_template('login.html', title='Sign In', login_form=login_form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        # Hashing the password here
        user.set_password(password=form.password.data)
        # Saving into database
        user.register()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))

    return render_template('register.html', title='Register', form=form)