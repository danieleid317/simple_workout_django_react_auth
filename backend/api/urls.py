from django.urls import path
from . import views

appname = "api"

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('workouts/', views.workouts),
    path('workout/<int:woid>/', views.workout),
    path('newworkout/', views.newworkout),
    path('addexercise/<int:woid>/', views.addexercise),
    path('exercise/<int:exercise_id>/', views.exercise),
    path('addset/<int:exercise_id>/', views.addset),

]
