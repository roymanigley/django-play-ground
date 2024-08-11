from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from core.models import Movie


class MovieTestCase(TestCase):

    def setUp(self):
        user = User(
            username='user',
            is_superuser=True,
        )
        user.set_password('password')
        user.save()
        self.client.login(username='user', password='password')

    def test_find_all_movies(self):
        # GIVEN
        movies = [
            {'name': 'The Matrix', 'price_per_day': 3.5},
            {'name': 'Forest Gump', 'price_per_day': 4.5},
            {'name': 'R.I.P Department', 'price_per_day': 1.5},
            {'name': 'The Lion Kong', 'price_per_day': 6.5},
            {'name': 'Lupin', 'price_per_day': 5.5},
        ]
        [Movie.objects.create(**movie) for movie in movies]
        # WHEN
        response = self.client.get('/api/movies/')
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        data = response.json()
        self.assertEqual(data['count'], 5)
        self.assertEqual(len(data['results']), 5)

    def test_filter_exact_movies(self):
        # GIVEN
        movies = [
            {'name': 'The Matrix', 'price_per_day': 3.5},
            {'name': 'Forest Gump', 'price_per_day': 4.5},
            {'name': 'R.I.P Department', 'price_per_day': 1.5},
            {'name': 'The Lion Kong', 'price_per_day': 6.5},
            {'name': 'Lupin', 'price_per_day': 5.5},
        ]
        [Movie.objects.create(**movie) for movie in movies]
        # WHEN
        response = self.client.get('/api/movies/?name=Lupin')
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['results']), 1)

    def test_filter_contains_movies(self):
        # GIVEN
        movies = [
            {'name': 'The Matrix', 'price_per_day': 3.5},
            {'name': 'Forest Gump', 'price_per_day': 4.5},
            {'name': 'R.I.P Department', 'price_per_day': 1.5},
            {'name': 'The Lion Kong', 'price_per_day': 6.5},
            {'name': 'Lupin', 'price_per_day': 5.5},
        ]
        [Movie.objects.create(**movie) for movie in movies]
        # WHEN
        response = self.client.get('/api/movies/?name__icontains=AtRi')
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['results']), 1)

    def test_create_movie(self):
        # GIVEN
        payload = {
            'name': 'The Matrix',
            'price_per_day': 3.5
        }
        # WHEN
        response = self.client.post('/api/movies/', data=payload)
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )
        data = response.json()
        self.assertEqual(data['name'], 'The Matrix')
        self.assertEqual(data['price_per_day'], 3.5)

    def test_update_movie(self):
        # GIVEN
        model = Movie.objects.create(name='The Matrix', price_per_day=3.5)
        payload = {
            'name': 'The Matrix Reloaded',
            'price_per_day': 5
        }
        # WHEN
        response = self.client.put(
            f'/api/movies/{model.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        data = response.json()
        self.assertEqual(data['name'], 'The Matrix Reloaded')
        self.assertEqual(data['price_per_day'], 5)

    def test_partial_update_movie(self):
        # GIVEN
        model = Movie.objects.create(name='The Matrix', price_per_day=3.5)
        payload = {
            'price_per_day': 5
        }
        # WHEN
        response = self.client.patch(
            f'/api/movies/{model.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        data = response.json()
        self.assertEqual(data['name'], 'The Matrix')
        self.assertEqual(data['price_per_day'], 5)

    def test_delete_movie(self):
        # GIVEN
        model = Movie.objects.create(name='The Matrix', price_per_day=3.5)
        # WHEN
        response = self.client.delete(f'/api/movies/{model.id}/')
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.content
        )
        self.assertIsNone(Movie.objects.filter(id=model.id).first())
