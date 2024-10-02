"""
URL configuration for buddypair project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('main_admin/', admin.site.urls),
    path('auth/', include("U_auth.urls")),
    # path(' ', include("U_auth.urls")),
    path('job/', include('job.urls')),  # This includes job.urls
    path('home/', include("matrimony_Home.urls")),
    path('profiles/', include("matrimony_profiles.urls")),
    path('subscription/', include("dating_subscription.urls")),
    path('U_messages/', include("matrimony_U_messages.urls")),
    path('admin/', include("matrimony_admin.urls")),
    path('accounts/', include('allauth.urls')),
    path('dating_home/', include('dating_home.urls')),  # Add a slash after 'dating_home'
    path('dating_rightmenubar/',include('dating_rightmenubar.urls')),
    path('dating_profiles/',include('dating_profiles.urls')),
    path('mtsubscription/', include("matrimony_subscriptions.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Add this at the end to link to custom 404 handler
handler404 = 'U_auth.views.error_404'
handler500 = 'U_auth.views.error_500'  # Custom 500 error handler