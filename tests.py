import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models import Student, Subject, Task
import os
from flask import abort, url_for

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://dt_admin:dt2020@localhost/dreamteam_test'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = Student(username="admin", password="admin2020", is_admin=True)

        # create test non-admin user
        student = Student(username="test_user", password="test2020")

        # save users to database
        db.session.add(admin)
        db.session.add(student)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()



if __name__ == "__main__":
    unittest.main()