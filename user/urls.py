from django.urls import path
from . import views

urlpatterns = [
    path('create-account/', views.CreateAccountView.as_view(), name='create-account'),
    path('activate/<uid64>/<token>/', views.activate, name='activate'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact_us'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
]
