# ipo_backend/ipo_app/urls.py

from django.urls import path
from .views import get_ipo_data

urlpatterns = [
    path('api/ipoData/', get_ipo_data, name='get_ipo_data'),
]
