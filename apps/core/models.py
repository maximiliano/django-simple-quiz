from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Quiz(TimestampedModel):
    name = models.CharField(_('name'), max_length=50)
    intersticial_text = models.TextField(_('intersticial text'))

    class Meta:
        verbose_name = _('quiz')
        verbose_name_plural = _('quizes')

    def __str__(self):
        return self.name


class QuizQuestion(TimestampedModel):
    order = models.PositiveSmallIntegerField(_('order'))
    video_url = models.URLField(null=True, blank=True)
    question = models.CharField(_('question'), max_length=256)
    question_slug = models.CharField(_('question_slug'), max_length=30)
    quiz = models.ForeignKey(
        Quiz,
        related_name='questions',
        on_delete=models.CASCADE,
        verbose_name=_('quiz'),
    )

    class Meta:
        ordering = ('order',)
        verbose_name = _('quiz question')
        verbose_name_plural = _('quiz questions')

    def __str__(self):
        return self.question


class QuizQuestionChoice(TimestampedModel):
    order = models.PositiveSmallIntegerField(_('order'))
    answer = models.CharField(_('answer'), max_length=256)
    answer_slug = models.CharField(_('answer_slug'), max_length=30)
    answer_feedback = models.CharField(_('answer feedback'), max_length=256)
    quiz_question = models.ForeignKey(
        QuizQuestion,
        related_name='choices',
        on_delete=models.CASCADE,
        verbose_name=_('quiz question'),
    )

    class Meta:
        ordering = ('order',)
        verbose_name = _('quiz question choice')
        verbose_name_plural = _('quiz questions choice')

    def __str__(self):
        return self.answer


class QuizAnswerSession(TimestampedModel):
    name = models.CharField(_('name'), max_length=50)
    email = models.EmailField(_('email'))
    quiz = models.ForeignKey(
        Quiz,
        related_name='answers',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('quiz'),
    )
    answer_data = models.JSONField(_('answer data'), default=dict)

    class Meta:
        verbose_name = _('quiz answer session')
        verbose_name_plural = _('quiz answer sessions')

    def __str__(self):
        return f'Quiz: {self.quiz.name} - Answer from {self.email}'
