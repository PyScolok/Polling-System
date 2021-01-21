from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PollsViewSet, QuestionsListView, QuestionDetailView


router = DefaultRouter()
router.register('polls', PollsViewSet, basename='polls')

urlpatterns = [
    path('polls/<int:pk>/questions/', QuestionsListView.as_view(), name='questions'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
]

urlpatterns += router.urls
