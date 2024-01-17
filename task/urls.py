from django.urls import path
from . import views

urlpatterns = [
    path('category/add/', views.AddCategoryView.as_view(), name='add-category'),
    path('add/', views.AddTaskView.as_view(), name='add-task'),
    path('edit/<int:id>', views.EditTaskView.as_view(), name='edit-task'),
    path('delete/<int:id>', views.deleteTask, name='delete-task'),
    path('completed/<int:id>', views.taskdone, name='task-done'),

]
