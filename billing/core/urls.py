from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core import views

urlpatterns = [
    path("health/", views.HealthCheckView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
