from django.urls import path
from .views.auth import UserAPI, LoginAPI
from .views.resource import ResourceAPI

urlpatterns = [
    path("users/", UserAPI.as_view(), name="users"),
    path("users/<int:pk>/", UserAPI.as_view(), name="users"),
    path("resources/", ResourceAPI.as_view(), name='resources'),
    path("resources/<int:pk>/", ResourceAPI.as_view(), name='resources'),
    path("login", LoginAPI.as_view(), name="login"),

]
