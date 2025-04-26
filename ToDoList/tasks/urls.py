from django.urls import path, include
from . import views

urlpatterns = [
    path("tasks/", views.TaskListCreateView.as_view()),
    path("tasks/<int:pk>/", views.TaskRetrieveUpdateDeleteView.as_view()),
    path("tasks/<int:pk>/complete/", views.mark_completed),
    path("tasks/<int:pk>/uncomplete/", views.mark_uncompleted),
    path("tasks/<int:pk>/priority/", views.update_priority),
]
