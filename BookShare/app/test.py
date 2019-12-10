import unittest
from app import app

class MyTestCase(unittest.TestCase):
    def test_login(self):
        with app.test_client() as client:
            response = client.post('/login/', data=dict(   # Use the client client to simulate sending web requests
                username='A',
                password='123456'
            ), follow_redirects=True)
            assert response.status_code == 200              # The assertion is 200

    def test_login_second(self):
        with app.test_client() as client:
            response = client.post('/login/', data=dict(  # Use the client client to simulate sending web requests
                username='12345687@@@@@',
                password='55555555555555555'
            ), follow_redirects=True)
            assert response.status_code == 200  # The assertion is 200

    # Test the registry to determine the response and status codes returned
    def test_register(self):
        with app.test_client() as client:
            response = client.post('/register/', data=dict(
                username='abc',
                password='1234'
            ), follow_redirects=True)
            assert response.status_code == 200

    def test_register_second(self):  # Test the registry to determine the response and status codes returned
        with app.test_client() as client:
            response = client.post('/register/', data=dict(
                username='sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss',
                password='1234'
            ), follow_redirects=True)
            assert response.status_code == 200

    # Test the post access /my_book/ to determine the response and status code returned
    def test_post_mybook(self):
        with app.test_client() as client:
            response = client.post('/my_book/', data=dict(
                title='1234',
                authdescripitionor='1234',
                author="abc",
                math=True
            ), follow_redirects=True)
            assert response.status_code == 200

    def test_post_mybook_second(self):
        with app.test_client() as client:
            response = client.post('/my_book/', data=dict(
                title='sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss',
                authdescripitionor='1234',
                author="abc",
                math=True
            ), follow_redirects=True)
            assert response.status_code == 200

    # test get method to get new
    def test_get_mybook(self):
        with app.test_client() as client:
            response = client.get('/my_book/')
            assert response.status_code == 302

if __name__ == '__main__':
    unittest.main()