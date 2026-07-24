from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Education, Experience, PortfolioItem, Skill, StudentProfile, User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('CampusCollab', {'fields': ('role','is_suspended','profile_completed')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('CampusCollab', {'fields': ('email','role')}),)
    list_display = ('email','username','role','is_active','is_suspended')

admin.site.register([StudentProfile, Skill, Education, Experience, PortfolioItem])
