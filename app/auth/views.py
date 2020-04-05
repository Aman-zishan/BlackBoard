from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Student


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add a student to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        student = Student(email=form.email.data,username=form.username.data,first_name=form.first_name.data,last_name=form.last_name.data,password=form.password.data)

        # add employee to the database
        db.session.add(student)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log a student in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        student = Student.query.filter_by(email=form.email.data).first()
        if student is not None and student.verify_password(
                form.password.data):
            # log employee in
            login_user(student)
            if student.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log a student out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))