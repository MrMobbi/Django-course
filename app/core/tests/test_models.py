"""
Test for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test Model."""

    def test_create_user_with_email_successfull(self):
        """Test creating a user with an email successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            passeord=password,
        )

        self.assertEqual(user.email, email)
        self.asserTrue(user.check_password(password))
