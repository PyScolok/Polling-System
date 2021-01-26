from datetime import datetime

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import PollSerializer, QuestionSerializer, ChoiceSerializer, VoteSerializer
from .models import Poll, Question, Choice


class PollsViewSet(ModelViewSet):
    queryset = Poll.objects.filter(finish_date__gt=datetime.now().date())
    serializer_class = PollSerializer

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'destroy': [IsAuthenticated],
        'update': [IsAuthenticated],
        'retrieve': [AllowAny]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if request.user != poll.author:
            raise PermissionDenied('You can not delete this poll.')
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if request.user != poll.author:
            raise PermissionDenied('You can not change this poll.')
        return super().update(request, *args, **kwargs)


class QuestionsViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'destroy': [IsAuthenticated],
        'update': [IsAuthenticated],
        'retrieve': [AllowAny]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset = self.queryset.filter(poll=self.kwargs['poll_pk'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['pk'])
        if request.user != question.poll.author:
            raise PermissionDenied('You can not delete this question.')
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['pk'])
        if request.user != question.poll.author:
            raise PermissionDenied('You can not change this question.')
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['pk'])
        if request.user != question.poll.author:
            raise PermissionDenied('You can not create a question this poll.')
        return super().create(request, *args, **kwargs)


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

    def create(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['question_pk'])
        if request.user != question.poll.author:
            raise PermissionDenied('You can not create a choice for this question.')
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['question_pk'])
        if request.user != question.poll.author:
            raise PermissionDenied('You can not change this choice.')
        return super().update(request, *args, **kwargs)


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({'error': 'Wrong credentials'}, status=status.HTTP_400_BAD_REQUEST)


class VoteView(CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = ()
    authentication_classes = ()

    def create(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['question_pk'])
        answer = request.data.get('answer')
        print(question)
        if question.question_type == 'free':
            return super().create(request, *args, **kwargs)
        elif question.question_type == 'one':
            if answer in question.choices:
                return super().create(request, *args, **kwargs)
            else:
                return Response({'error': 'Wrong answer. Please choose a variant from the suggested.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            pass


