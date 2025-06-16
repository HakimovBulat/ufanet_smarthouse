from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("open", views.open, name="open"),
    path("call", views.call, name="call"),
    path("<int:pk>", views.intercom, name="intercom"),
]