from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Quiz(TimestampedModel):
    name = models.CharField(_('name'), max_length=50)

    class Meta:
        verbose_name = _('quiz')
        verbose_name_plural = _('quizes')


class QuizQuestion(TimestampedModel):
    order = models.PositiveSmallIntegerField(_('order'))
    question = models.CharField(_('question'), max_length=256)
    quiz = models.ForeignKey(
        Quiz,
        related_name='questions',
        on_delete=models.CASCADE,
        verbose_name=_('quiz'),
    )

    class Meta:
        verbose_name = _('quiz question')
        verbose_name_plural = _('quiz questions')


class QuizQuestionChoice(TimestampedModel):
    order = models.PositiveSmallIntegerField(_('order'))
    answer = models.CharField(_('answer'), max_length=256)
    answer_slug = models.CharField(_('answer_slug'), max_length=30)
    quiz_question = models.ForeignKey(
        QuizQuestion,
        related_name='choices',
        on_delete=models.CASCADE,
        verbose_name=_('quiz question'),
    )

    class Meta:
        verbose_name = _('quiz question choice')
        verbose_name_plural = _('quiz questions choice')


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
    answer_data = models.JSONField(_('answer data'))

    class Meta:
        verbose_name = _('quiz answer session')
        verbose_name_plural = _('quiz answer sessions')
