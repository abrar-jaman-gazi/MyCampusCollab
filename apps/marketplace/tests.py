from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from apps.accounts.models import Skill, User
from .models import Gig, GigCategory, Proposal
class MarketplaceTests(TestCase):
    def setUp(self):
        self.owner=User.objects.create_user(username='owner',email='owner@example.com',password='Pass12345!')
        self.applicant=User.objects.create_user(username='applicant',email='applicant@example.com',password='Pass12345!')
        cat=GigCategory.objects.create(name='Web',slug='web')
        self.gig=Gig.objects.create(owner=self.owner,category=cat,title='Build website',description='A complete responsive website.',budget=1000,deadline=timezone.localdate()+timedelta(days=10))
    def test_owner_cannot_apply(self):
        self.client.login(email='owner@example.com',password='Pass12345!')
        response=self.client.get(reverse('marketplace:submit_proposal',args=[self.gig.pk]))
        self.assertRedirects(response,self.gig.get_absolute_url())
    def test_applicant_can_submit_once(self):
        self.client.login(email='applicant@example.com',password='Pass12345!')
        data={'cover_letter':'I am ready to help.','proposed_cost':900,'delivery_days':7,'milestones':'Draft and delivery'}
        self.client.post(reverse('marketplace:submit_proposal',args=[self.gig.pk]),data)
        self.assertEqual(Proposal.objects.filter(gig=self.gig,applicant=self.applicant).count(),1)
