from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from apps.accounts.models import User
from .models import CollaborationProject, ProjectCategory, TeamMember
class CollaborationTests(TestCase):
    def setUp(self):
        self.owner=User.objects.create_user(username='lead',email='lead@example.com',password='Pass12345!')
        self.student=User.objects.create_user(username='member',email='member@example.com',password='Pass12345!')
        cat=ProjectCategory.objects.create(name='Research',slug='research')
        self.project=CollaborationProject.objects.create(owner=self.owner,category=cat,title='Research project',project_type='research',description='Study topic',roles_needed='Analyst',team_size=2,start_date=timezone.localdate(),end_date=timezone.localdate()+timedelta(days=30))
        TeamMember.objects.create(project=self.project,user=self.owner,role='Owner')
    def test_student_can_request_join(self):
        self.client.login(email='member@example.com',password='Pass12345!')
        response=self.client.post(reverse('collaboration:join_project',args=[self.project.pk]),{'role':'Analyst','message':'I can help.'})
        self.assertEqual(response.status_code,302)
        self.assertTrue(self.project.join_requests.filter(applicant=self.student).exists())
