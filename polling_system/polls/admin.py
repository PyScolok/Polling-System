from django.contrib import admin

from .models import Poll, Question, Choice


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'start_date', 'finish_date')
    search_fields = ('name', 'author')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('poll', 'question_text', 'question_type')
    search_fields = ('poll', 'question_type')
    list_filter = ('question_type', )
    save_as = True


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text')
    search_fields = ('choice_text', )
    save_as = True
