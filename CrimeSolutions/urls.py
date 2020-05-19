from django.urls import path
from . import views
from .views import ListActivitiesView

urlpatterns = [
    path("", views.launch, name="landing"),
    path("map", views.crime_map, name="idx_map"),
    path("index", views.index, name="index"),
    path("<int:activity_id>", views.activity, name="activity"),
    path("report", views.report, name="report"),
    path("endorse<int:activity_id>", views.endorse, name="endorse"),
    path("signup", views.signup, name='signup'),
    path('user', views.user, name='user'),
    path('api/activities', ListActivitiesView.as_view(), name="songs-all")

]
