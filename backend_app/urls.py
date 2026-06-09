from django.urls import path
from .views import health_check, process_image


urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('process-image/', process_image, name='process_image'),
]