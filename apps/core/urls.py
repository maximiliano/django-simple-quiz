from django.urls import path
from core import views

urlpatterns = [
    path('<int:pk>', views.LandingPageView.as_view(), name='landing_page'),
]
