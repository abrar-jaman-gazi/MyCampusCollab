from django.urls import path
from . import views
app_name='communication'
urlpatterns=[path('messages/',views.inbox,name='inbox'),path('messages/<int:conversation_id>/',views.inbox,name='conversation'),path('messages/<int:conversation_id>/send/',views.send_message,name='send_message'),path('start/<str:username>/',views.start_conversation,name='start'),path('notifications/',views.notifications,name='notifications'),path('notifications/<int:pk>/read/',views.notification_read,name='notification_read'),path('notifications/read-all/',views.mark_all_read,name='mark_all_read')]
