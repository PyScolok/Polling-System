from datetime import datetime

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from .serializers import PollSerializer, QuestionSerializer, ChoiceSerializer
from .models import Poll, Question, Choice


class PollsViewSet(ModelViewSet):
    queryset = Poll.objects.filter(finish_date__gt=datetime.now().date())
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if request.user != poll.author:
            raise PermissionDenied('You can not delete this poll.')
        return super().destroy(request, *args, **kwargs)


class QuestionsViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(poll=self.kwargs['poll_pk'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['pk'])
        if request.user != question.poll.author:
            raise PermissionDenied('You can not delete this question.')
        return super().destroy(request, *args, **kwargs)


class ChoicesViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(question=self.kwargs['question_pk'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['question_pk'])
        if request.user != question.poll.author:
            raise PermissionDenied('You can not delete this choice.')
        return super().destroy(request, *args, **kwargs)