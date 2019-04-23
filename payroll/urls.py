from django.urls import path

from . import views

urlpatterns = [
    path('', views.payroll_report, name='report'),
    path('upload/done/', views.upload_done, name='upload_done'),
    path('upload/', views.upload_file, name='upload'),
]
