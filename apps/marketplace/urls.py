from django.urls import path
from . import views
app_name='marketplace'
urlpatterns=[
 path('',views.gig_list,name='gig_list'),path('create/',views.gig_create,name='gig_create'),path('mine/',views.my_gigs,name='my_gigs'),path('proposals/mine/',views.my_proposals,name='my_proposals'),
 path('<int:pk>/',views.gig_detail,name='gig_detail'),path('<int:pk>/edit/',views.gig_edit,name='gig_edit'),path('<int:pk>/delete/',views.gig_delete,name='gig_delete'),path('<int:pk>/save/',views.save_gig,name='save_gig'),
 path('<int:pk>/apply/',views.submit_proposal,name='submit_proposal'),path('<int:pk>/proposals/',views.received_proposals,name='received_proposals'),path('proposal/<int:pk>/<str:status>/',views.proposal_status,name='proposal_status'),
]
