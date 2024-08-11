from django.test import TestCase
from rest_framework import status
from django.contrib.auth.models import User, Permission, Group
from rest_framework.authtoken.models import Token


class LoginTestCase(TestCase):

    def test_login_user_not_exist(self):
        # WHEN
        response = self.client.post(
            '/auth/token/', data={'username': 'user', 'password': '123456'}
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )

    def test_login_user_exist_wrong_password(self):
        # GIVEN
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()
        # WHEN
        response = self.client.post(
            '/auth/token/', data={'username': 'user', 'password': '123456'}
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.content
        )

    def test_login_user_exist_correct_password(self):
        # GIVEN
        user = User.objects.create(username='user')
        user.set_password('123456')
        user.save()
        # WHEN
        response = self.client.post(
            '/auth/token/', data={'username': 'user', 'password': '123456'}
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        data = response.json()
        self.assertIsNotNone(data['token'])


class UserTest(TestCase):

    def test_user_endpoint_normal_user(self):
        # GIVEN
        user = User.objects.create(username='normal-user')
        user.user_permissions.add(Permission.objects.all().first())
        group = Group.objects.create(name='test_group')
        group.permissions.add(Permission.objects.all()[1])
        user.groups.add(group)
        token = Token.objects.create(user=user)
        # WHEN
        response = self.client.get(
            '/auth/me/', headers={'Authorization': f'Token {token.key}'}
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        data = response.json()
        self.assertEqual(data['username'], 'normal-user')
        self.assertEqual(data['is_superuser'], False)
        self.assertEqual(len(data['groups']), 1)
        self.assertEqual(len(data['permissions']), 2)

    def test_user_endpoint_super_user(self):
        # GIVEN
        user = User.objects.create(username='super-user', is_superuser=True)
        token = Token.objects.create(user=user)
        # WHEN
        response = self.client.get(
            '/auth/me/', headers={'Authorization': f'Token {token.key}'}
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        data = response.json()
        self.assertEqual(data['username'], 'super-user')
        self.assertEqual(data['is_superuser'], True)
        self.assertEqual(len(data['groups']), 0)
        self.assertEqual(
            len(data['permissions']), Permission.objects.all().count()
        )
