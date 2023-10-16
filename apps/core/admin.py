from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core import models


class QuizQuestionInline(admin.TabularInline):
    model = models.QuizQuestion
    readonly_fields = ('id',)
    show_change_link = True
    extra = 3


@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'answers', 'created_at')
    inlines = [QuizQuestionInline]

    def answers(self, obj):
        return obj.answers.count()

    answers.short_description = _('Answers')


class QuizQuestionChoiceInline(admin.TabularInline):
    model = models.QuizQuestionChoice
    readonly_fields = ('id',)
    extra = 3


@admin.register(models.QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'choices', 'quiz', 'created_at')
    inlines = [QuizQuestionChoiceInline]

    def choices(self, obj):
        return obj.choices.count()

    choices.short_description = _('Choices')


admin.site.register(models.QuizAnswerSession)
