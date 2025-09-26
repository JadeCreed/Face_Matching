
from django.urls import path
from . import views

urlpatterns = [
    path('', views.students_list, name='students_list'),
    path('forms/', views.submit_student, name='forms'),
    path('upload_photos/', views.upload_photos, name='upload_photos'),
    path('delete_students/', views.delete_students, name='delete_students'),
    path("match-detail/<int:student_id>/", views.match_detail, name="match_detail"),
]
