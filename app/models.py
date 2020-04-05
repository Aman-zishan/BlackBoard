# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class Student(UserMixin, db.Model):
    """
    Create an student table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Student: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


class Subject(db.Model):
    """
    Create a Subject table
    """

    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    student = db.relationship('Student', backref='subject',lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Task(db.Model):
    """
    Create a Task table
    """

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    student = db.relationship('Student', backref='task',lazy='dynamic')

    def __repr__(self):
        return '<Task: {}>'.format(self.name)