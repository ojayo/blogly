from app import app
from unittest import TestCase
from flask import Flask, request, render_template, redirect
from models import User, db, connect_db



# we put random.randint to get a random id to test with
# if we need to run the tests multiple times
# but this isn't ideal in a real world situation 
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
connect_db(app)



# could avoid testing id by using other elements that you know 
# for example, if you want to test if you added a user, can look 
# at how many users there are and then see if the amount increments by 1
# vice versa for deleting a user

# should make a test user to test viewing and deleting the user routes
# it pulls directly from the database so it would be an issue
# if we don't have any existing user to test with
# also have to pass in a specific user to test


class BloglyTestCase(TestCase):
    """ integration tests with blogly app """
    def setUp(self):
        db.create_all()
        test_user = User(id=980, first_name='Whiskey', last_name='9000', image_url='')
        db.session.add(test_user)
        db.session.commit()
        

    def test_users_page(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add User', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add', html)

    def test_user_detail_page(self):
        with app.test_client() as client:
            resp = client.get('/users/980')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Posts</h1>', html)

    def test_delete_redirect(self):
        with app.test_client() as client:
            resp = client.post("/users/980/delete")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users")

    def tearDown(self):
        db.drop_all()
