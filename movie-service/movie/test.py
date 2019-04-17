from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from . models import Movie, List


def setup_user():
    User = get_user_model()
    return User.objects.create_user(
        'test',
        email='test@test.com',
        password='test'
    )



class TestMovie(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        Movie.objects.create(title="test_movie1", director="kevin")

    def test_post_single_movie(self):
        self.client.login(username="test", password="test")
        uri = '/api/v1/movie/'
        params = {'title':'test_movie2', 'director': 'kevin liu'}
        response = self.client.post(uri, params)
        self.assertEqual(
            response.status_code, 201,
            "Expeted Response Code 201, received {0} instead.".format(response.status_code)
        )

    def test_list_all_movie(self):
        self.client.login(username="test", password="test")
        uri = '/api/v1/movie/'
        response = self.client.get(uri)
        self.assertEqual(
            response.status_code, 200,
            "Expeted Response Code 200, received {0} instead.".format(response.status_code)
        )

    def test_list_single_movie(self):
        self.client.login(username="test", password="test")
        uri = '/api/v1/movie/1/'
        response = self.client.get(uri)
        self.assertEqual(
            response.status_code, 200,
            "Expeted Response Code 200, received {0} instead.".format(response.status_code)
        )
        self.assertEqual(
            response.data['title'], 'test_movie1',
            "Expected resulting movie title as test_movie1, but received {} instead.".format(response.data['title'])
        )



class TestList(APITestCase):
    """
    Another way to test with APIClient.
    You use it as an client tester. You have to specify the full uri.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        List.objects.create(name="test_list", user=self.user)
        Movie.objects.create(title="movie1", director="kevin")


    def test_list_single_list(self):
        self.client.login(username="test", password="test")
        uri = '/api/v1/list/1/'
        response = self.client.get(uri)
        self.assertEqual(
            response.status_code, 200,
            "Expected Response Code 200, received {status_code} instead. error message: {reasone}".format(status_code=response.status_code, reasone=response.reason_phrase)
        )
        self.assertEqual(
            response.data['name'], 'test_list',
            "Expected test_list, git {name} instead.".format(name=response.data['name'])
        )

    def test_list_of_lists(self):
        self.client.login(username="test", password="test")
        uri = '/api/v1/list/'
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 200,
                    'Expected Response Code 200, received {0} instead.'
                    .format(response.status_code))

    def test_post_new_list(self):
        self.client.login(username="test", password="test")
        uri = '/api/v1/list/'
        params = {
            "name": "test-list"
        }
        response = self.client.post(uri, params)
        self.assertEqual(
            response.status_code, 201,
            "Expeted Response Code 201, received {0} instead.".format(response.status_code)
        )

    def test_save_movie_to_list(self):
        self.client.login(username="test", password="test")
        uri = '/api/v1/movie/1/save/'
        response = self.client.post(uri)
        self.assertEqual(
            response.status_code, 201,
            "Expected Response Code 201, got {status_code} instead. Data: {data}".format(data=response.data,status_code=response.status_code)
        )