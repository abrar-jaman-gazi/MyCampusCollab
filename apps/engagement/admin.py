from django.contrib import admin
from .models import AdminAction, Report, Review
admin.site.register([AdminAction, Report, Review])
