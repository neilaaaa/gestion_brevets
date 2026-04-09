from django.urls import path
from .views import DashboardCountView

urlpatterns = [
    path("counts/", DashboardCountView.as_view(), name="dashboard-counts"),
]