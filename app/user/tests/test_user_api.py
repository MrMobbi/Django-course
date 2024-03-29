"""
Test for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public feature of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'email':    'test@example.com',
            'password': 'testpass123',
            'name':     'Test User',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email':    'test1@example.com',
            'password': 'testpass123',
            'name':     'Test User',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password too short."""
        payload = {
            'email':    'test2@exmaple.com',
            'password': 'pw',
            'name':     'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generate token valid credentials."""
        user_detail = {
            'name':     'Test User',
            'email':    'test3@example.com',
            'password': 'testpass123',
        }
        create_user(**user_detail)

        payload = {
            'email':    user_detail['email'],
            'password': user_detail['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalids."""

        user_detail = {
            'name':     'Test User',
            'email':    'test4@example.com',
            'password': 'goodpass',
        }
        create_user(**user_detail)
        payload = {
            'email': user_detail['email'],
            'password': 'badpass1',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test returns error if a blank passord is posted"""
        user_detail = {
            'name':     'Test User',
            'email':    'test5@example.com',
            'password': '',
        }
        create_user(**user_detail)
        payload = {
            'email': user_detail['email'],
            'password': user_detail['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
