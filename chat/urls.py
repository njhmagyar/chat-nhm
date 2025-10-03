from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatSessionViewSet, CommonQuestionsViewSet

router = DefaultRouter()
router.register(r'sessions', ChatSessionViewSet)
router.register(r'questions', CommonQuestionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]