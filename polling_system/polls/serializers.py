from rest_framework import serializers

from .models import Vote, Question, Poll, Choice


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = '__all__'
        extra_kwargs = {'question': {'required': False}}


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = '__all__'
