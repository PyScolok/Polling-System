from datetime import datetime

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from .serializers import PollSerializer, QuestionSerializer
from .models import Poll, Question


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
        queryset = Question.objects.filter(poll=self.kwargs['poll_pk'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['pk'])
        if request.user != question.poll.author:
            raise PermissionDenied('You can not delete this question.')
        return super().destroy(request, *args, **kwargs)
