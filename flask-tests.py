from unittest import TestCase

from app import app
from models import db, User

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly-test"
app.config["SQLALCHEMY_ECHO"] = False

app.config["TESTING"] = True

db.drop_all()
db.create_all()

class BloglyViewTestCase(TestCase):
    '''Test views for Users'''

    def setUp(self):
        User.query.delete()

        user = User(first_name='Test', last_name='Testerson', img_url='https://sample.com')
        db.session.add(user)
        db.session.commit()

        self.user_id = id

    def tearDown(self):
        db.session.rollback()

    def test_users_list(self):
        with app.test_client as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_user_details(self):
        with app.test_client as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Testerson</h1>', html)

    def test_add_user(self):
        with app.test_client as client:
            u = {'first_name': 'Test2', 'last_name': 'Testy'}
            resp = client.post('/users/new', data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test2 Testy</h1>', html)