from django.urls import path
from . import views
app_name='dashboard'
urlpatterns=[path('',views.dashboard_home,name='home'),path('admin/',views.admin_home,name='admin_home'),path('admin/users/',views.admin_users,name='admin_users'),path('admin/users/<int:pk>/suspend/',views.toggle_suspend,name='toggle_suspend'),path('admin/content/',views.admin_content,name='admin_content'),path('admin/content/<str:kind>/<int:pk>/toggle/',views.toggle_content,name='toggle_content'),path('admin/reports/',views.admin_reports,name='admin_reports'),path('admin/reports/<int:pk>/<str:status>/',views.resolve_report,name='resolve_report')]
