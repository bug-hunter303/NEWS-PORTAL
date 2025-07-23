from django.urls import path
from news_portal import views

urlpatterns = [
    path("", views.HomeView.as_view(),name="home"),
]