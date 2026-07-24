from django.test import TestCase
from django.urls import reverse
from .models import User

class AccountFlowTests(TestCase):
    def test_register_creates_profile(self):
        response=self.client.post(reverse('accounts:register'),{'first_name':'Test','last_name':'Student','username':'teststudent','email':'test@example.com','password1':'StrongPass123!','password2':'StrongPass123!'})
        self.assertEqual(response.status_code,302)
        user=User.objects.get(email='test@example.com')
        self.assertTrue(hasattr(user,'profile'))
