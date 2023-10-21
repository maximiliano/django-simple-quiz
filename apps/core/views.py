from django.views.generic import DetailView

from core.models import Quiz


class LandingPageView(DetailView):
    template_name = 'core/landing_page.html'
    model = Quiz
