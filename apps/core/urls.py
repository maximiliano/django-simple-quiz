from django.urls import path

from core import views

urlpatterns = [
    path('<int:pk>/', views.LandingPageView.as_view(), name='landing_page'),
    path(
        '<int:pk>/registration/',
        views.Registration.as_view(),
        name='registration',
    ),
    path(
        '<int:pk>/intersticial/',
        views.IntersticialPageView.as_view(),
        name='intersticial',
    ),
    path(
        '<int:pk>/question/<int:order>/',
        views.QuestionPageView.as_view(),
        name='question',
    ),
]
