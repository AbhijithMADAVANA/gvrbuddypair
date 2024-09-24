# urls.py
from django.urls import path
from . import views  # Make sure views are imported

urlpatterns = [
    path('hh/', views.hh, name="hh"),  # No parentheses after views.hh
    # Other URL patterns...
]
