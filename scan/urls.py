from django.urls import path
from . import views

urlpatterns = [
    path('imgscan/', views.image_scan, name='image_scan'),
    path('predict-image/', views.predict_image, name='predict_image'),
    path('audscan/', views.audio_scan, name='audio_scan'),
]
