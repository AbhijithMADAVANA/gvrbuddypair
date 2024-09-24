from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views
from django.contrib.auth import views as auth_views


app_name = 'dating_rightmenubar'

urlpatterns=[
    path('sent_request/', SentRequestView.as_view(), name='sent_request'),
    path('accept_request/', AcceptRequestView.as_view(), name='accept_request'),
    path('reject_request/', RejectRequestView.as_view(), name='reject_request'),
    path('recived_request/', ReceivedRequestView.as_view(), name='recived_request'),

    path('shortlisted_by/', ShortListedByView.as_view(), name='shortlisted_by'),
    path('shortlist/', ShortListedView.as_view(), name='shortlist'),
    path('remove-shortlist/<int:pk>/', RemoveShortlistedcostume_userView.as_view(), name='remove_from_shortlist'),

    # path('remove-shortlist/<int:pk>/', RemoveShortlistedUserView.as_view(), name='remove_from_shortlist'),
    # path('shortlist/<int:pk>/', ShortlistUserView.as_view(), name='shortlist-user'),

    path('contacted/', ContactedView.as_view(), name='contacted'),
    path('viewed_profile/', ViewedProfileView.as_view(), name='viewed_profile'),
   
    path('send_connection_request/<int:user_id>/', SendConnectionRequestView.as_view(), name='send_connection_request'),
    path('accept_connection_request/<int:request_id>/', AcceptConnectionRequestView.as_view(), name='accept_connection_request'),
    path('decline_connection_request/<int:request_id>/', DeclineConnectionRequestView.as_view(), name='decline_connection_request'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



