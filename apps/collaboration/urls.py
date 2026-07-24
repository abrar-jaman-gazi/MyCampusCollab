from django.urls import path
from . import views
app_name='collaboration'
urlpatterns=[
 path('',views.project_list,name='project_list'),path('create/',views.project_create,name='project_create'),path('mine/',views.my_projects,name='my_projects'),
 path('<int:pk>/',views.project_detail,name='project_detail'),path('<int:pk>/edit/',views.project_edit,name='project_edit'),path('<int:pk>/delete/',views.project_delete,name='project_delete'),path('<int:pk>/join/',views.join_project,name='join_project'),path('<int:pk>/team/',views.team_manage,name='team_manage'),path('<int:pk>/update/',views.add_update,name='add_update'),path('<int:pk>/members/<int:member_id>/remove/',views.remove_member,name='remove_member'),
 path('join-request/<int:pk>/<str:status>/',views.join_request_status,name='join_request_status'),
]
