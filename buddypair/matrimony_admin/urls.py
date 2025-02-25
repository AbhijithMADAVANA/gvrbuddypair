from django.urls import path
from . import views

app_name='custom_admin'

urlpatterns =[
    path('admin_login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('admin_logout/', views.AdminLogoutView.as_view(), name='admin_logout'),
    path('admin_home/', views.AdminHomeView.as_view(), name="admin_home"),
    path('financial_management/',views.FinancialManagement.as_view(), name='financial_management'),
    path('user/', views.usr_mng, name="user_management"),
    path('notification_management/',views.NotifcationManagement.as_view(),name='notification_management'),
    path('admin_profile/', views.admin_profile.as_view(), name="admin_profile"),
]