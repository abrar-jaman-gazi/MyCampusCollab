from django.contrib import admin
from .models import CollaborationProject, JoinRequest, ProjectCategory, ProjectUpdate, TeamMember
admin.site.register([CollaborationProject, JoinRequest, ProjectCategory, ProjectUpdate, TeamMember])
