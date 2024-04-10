from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),

    path("", views.TaksListView.as_view(), name="index"),
    path("add/", views.CreateTaskView.as_view(), name="add"),
    path("task/<int:pk>/", views.TaksDetailView.as_view(), name="task"),
    path("update/<int:pk>/", views.UpdateTaskView.as_view(), name="update"),
    path("delete/<int:pk>/", views.DeleteTaskView.as_view(), name="delete"),
]
