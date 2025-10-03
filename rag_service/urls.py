from django.urls import path
from .views import SuggestedQuestionsView, TestRetrievalView

urlpatterns = [
    path('suggested-questions/', SuggestedQuestionsView.as_view(), name='suggested-questions'),
    path('test-retrieval/', TestRetrievalView.as_view(), name='test-retrieval'),
]