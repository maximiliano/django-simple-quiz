from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from core.models import Quiz, QuizAnswerSession


class LandingPageView(DetailView):
    template_name = 'core/landing_page.html'
    model = Quiz


class Registration(CreateView):
    template_name = 'core/registration.html'
    model = QuizAnswerSession
    fields = ('name', 'email', 'quiz')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.quiz = get_object_or_404(Quiz, pk=kwargs.get('pk', 0))

    def get_initial(self):
        return {'quiz': self.quiz.pk}

    def form_valid(self, form):
        response = super().form_valid(form)
        max_age = 30 * 24 * 60 * 60  # 30 days
        response.set_cookie('quiz_identifier', self.object.pk, max_age=max_age)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = self.quiz
        return context

    def get_success_url(self):
        return reverse('intersticial', kwargs={'pk': self.object.pk})


class IntersticialPageView(DetailView):
    template_name = 'core/intersticial.html'
    model = Quiz
