from django.urls import path

from . import views
app_name = 'dating_profiles'

urlpatterns = [
    path('dtprofile/<int:user_id>/',views.UserProfileView.as_view(), name="profile"),
    path('profile_viewers/',views.ProfileViewersListView.as_view(), name='profile_viewers'),
    # path('msg_pg',views.messages_pg, name="msg_pg"),
    path('dtsend/<int:pk>/',views.SendRequestView.as_view(), name="send_request"),
    path('dtsent/',views.SentedRequestView.as_view(), name="sented_request"),
    path('dtaccept/',views.AcceptedRequestView.as_view(), name="accepted_request"),
    path('dtreject/',views.RejectedRequestView.as_view(), name="rejected_request"),
    path('dtreceived/',views.ReceivedRequestView.as_view(), name="received_request"),
    # path('dtrequest-hanlde/<int:pk>/<str:action>/', views.HandleRequestView.as_view(), name='handle_request'),
    path('dtrequest-handle/<int:pk>/<str:action>/', views.HandleRequestView.as_view(), name='handle_request'),
    path("dtrequest/delete/<int:pk>", views.DeleteRequestView.as_view(), name="delete_request"),
    path('dtshortlist/', views.ShortlistView.as_view(), name='shortlist'),
    path('dtshortlist/add/<int:user_id>/', views.AddToShortlistView.as_view(), name='add_to_shortlist'),
    path('dtshortlist/remove/<int:user_id>/', views.RemoveFromShortlistView.as_view(), name='remove_from_shortlist'),
    path('dtshortlist_by/', views.ShortlistByView.as_view(), name='shortlist_by'),
    # path('chat',views.user_chat_pg, name="chat"),
    # path('contacted',views.user_contacted_pg, name="contacted"),
    # path('shortlisted',views.user_shortlisted_pg, name="shortlisted"),
    # path('shortlist',views.user_shortlist_pg, name="shortlist"),
    # path('pr_viewed',views.user_viewed_pg, name="pr_viewed"),

    
]