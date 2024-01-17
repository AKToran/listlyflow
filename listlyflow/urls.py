from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.home, name='sort-category'),
    path('priority/<str:bool>/', views.sortByPriority, name='sort-priority'),
    path('user/', include('user.urls')),
    path('task/', include('task.urls')),
]
