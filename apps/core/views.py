from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView

from core.models import (
    Quiz,
    QuizQuestion,
    QuizAnswerSession,
    QuizQuestionChoice,
)


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
        return reverse('intersticial', kwargs={'pk': self.quiz.pk})


class IntersticialPageView(DetailView):
    template_name = 'core/intersticial.html'
    model = Quiz


class QuestionPageView(TemplateView):
    template_name = 'core/question.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.quiz = get_object_or_404(Quiz, pk=kwargs.get('pk', 0))
        self.order = kwargs.get('order', 1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = self.quiz
        return context

    def get(self, request, *args, **kwargs):
        question = get_object_or_404(
            QuizQuestion, quiz=self.quiz, order=kwargs.get('order', 1)
        )
        context = {'question': question}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        question = QuizQuestion.objects.get(
            order=self.order, quiz_id=self.quiz.pk
        )
        answer = get_object_or_404(
            QuizQuestionChoice,
            quiz_question_id=question.pk,
            answer_slug=request.POST.get('answer'),
        )
        answer_session_pk = request.COOKIES.get('quiz_identifier')

        answer_session = QuizAnswerSession.objects.get(pk=answer_session_pk)
        data = answer_session.answer_data
        data[question.order] = {
            'question_slug': question.question_slug,
            'answer_slug': answer.answer_slug,
        }
        answer_session.answer_data = data
        answer_session.save(update_fields=['answer_data'])

        url = reverse(
            'question',
            kwargs={'pk': self.quiz.pk, 'order': self.order + 1},
        )
        return redirect(url)
