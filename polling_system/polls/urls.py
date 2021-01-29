from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import PollsViewSet, QuestionsViewSet, ChoicesViewSet, LoginView, VoteView, CompletePollsView


router = DefaultRouter()
router.register('polls', PollsViewSet, basename='polls')

questions_router = routers.NestedSimpleRouter(router, r'polls', lookup='poll')
questions_router.register('questions', QuestionsViewSet)

choices_router = routers.NestedSimpleRouter(questions_router, r'questions', lookup='question')
choices_router.register('choices', ChoicesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(questions_router.urls)),
    path('', include(choices_router.urls)),
    path('polls/<int:poll_pk>/questions/<int:question_pk>/vote/', VoteView.as_view(), name='vote'),
    path('polls/<int:poll_pk>/answers/<int:respondent_id>/', CompletePollsView.as_view(), name='complete_polls'),
    path('login/', LoginView.as_view(), name='login')
]

