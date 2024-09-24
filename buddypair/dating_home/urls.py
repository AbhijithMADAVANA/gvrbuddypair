from django.urls import path
from . views import *

urlpatterns = [
    path('home/', HomeView.as_view(),name="home1"),
    path('entry',EntryView.as_view(),name="entry"),
    path('sharedslidbar',SharedSlidbar.as_view(),name="sharedslidbar"),
   

]