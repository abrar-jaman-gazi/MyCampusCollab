from django.contrib import admin
from .models import Gig, GigCategory, Proposal, SavedGig
admin.site.register([Gig, GigCategory, Proposal, SavedGig])
