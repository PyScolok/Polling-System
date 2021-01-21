from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Poll(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    description = models.TextField(blank=True)
    start_date = models.DateField(auto_now_add=True)
    finish_date = models.DateField()

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_TYPES = (
        ('free', 'free answer'),
        ('one', 'one answer'),
        ('many', 'several answers'),
    )

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=255, choices=QUESTION_TYPES)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    respondent_id = models.PositiveIntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes')
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.answer
