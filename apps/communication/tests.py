from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import User
from .models import Conversation
class MessagingPermissionTests(TestCase):
    def test_non_participant_cannot_open_conversation(self):
        a=User.objects.create_user(username='a',email='a@example.com',password='Pass12345!')
        b=User.objects.create_user(username='b',email='b@example.com',password='Pass12345!')
        c=User.objects.create_user(username='c',email='c@example.com',password='Pass12345!')
        conv=Conversation.objects.create();conv.participants.add(a,b)
        self.client.login(email='c@example.com',password='Pass12345!')
        self.assertEqual(self.client.get(reverse('communication:conversation',args=[conv.pk])).status_code,404)
