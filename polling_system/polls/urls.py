from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import PollsViewSet, QuestionsViewSet


router = DefaultRouter()
router.register('polls', PollsViewSet, basename='polls')

questions_router = routers.NestedSimpleRouter(router, r'polls', lookup='poll')
questions_router.register('questions', QuestionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(questions_router.urls))
]

