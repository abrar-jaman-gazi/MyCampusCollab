from django.urls import path
from . import views
app_name='engagement'
urlpatterns=[path('review/<str:username>/',views.review_create,name='review_create'),path('report/',views.report_create,name='report_create')]
