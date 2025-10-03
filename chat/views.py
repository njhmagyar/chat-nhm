from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import time
import uuid

from .models import ChatSession, ChatMessage, CommonQuestions
from .serializers import (
    ChatSessionSerializer, ChatSessionSummarySerializer,
    ChatMessageSerializer, SendMessageSerializer, CommonQuestionsSerializer
)
from rag_service.chat_service import ChatService


@method_decorator(csrf_exempt, name='dispatch')
class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ChatSessionSummarySerializer
        return ChatSessionSerializer
    
    def create(self, request):
        """Create a new chat session"""
        session = ChatSession.objects.create(
            user_ip=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Create welcome message
        welcome_message = ChatMessage.objects.create(
            session=session,
            message_type='assistant',
            content="Hi! I'm here to help you learn about my design work and experience. You can ask me about my projects, skills, design process, or anything else you'd like to know!",
            response_type='text'
        )
        
        session.total_messages = 1
        session.save()
        
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message and get AI response"""
        session = get_object_or_404(ChatSession, pk=pk)
        
        serializer = SendMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_message = serializer.validated_data['message']
        
        # Create user message
        user_msg = ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=user_message
        )
        
        # Generate AI response
        start_time = time.time()
        try:
            chat_service = ChatService()
            response_data = chat_service.generate_response(user_message, session.id)
            
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Create assistant response
            assistant_msg = ChatMessage.objects.create(
                session=session,
                message_type='assistant',
                content=response_data['content'],
                response_type=response_data.get('response_type', 'text'),
                referenced_projects=response_data.get('referenced_projects', []),
                referenced_skills=response_data.get('referenced_skills', []),
                referenced_experiences=response_data.get('referenced_experiences', []),
                media_urls=response_data.get('media_urls', []),
                retrieval_context=response_data.get('retrieval_context'),
                confidence_score=response_data.get('confidence_score'),
                response_time_ms=response_time_ms
            )
            
            # Update session
            session.total_messages += 2
            session.updated_at = timezone.now()
            session.save()
            
            # Return both messages
            return Response({
                'user_message': ChatMessageSerializer(user_msg).data,
                'assistant_message': ChatMessageSerializer(assistant_msg).data,
                'session_updated': ChatSessionSummarySerializer(session).data
            })
            
        except Exception as e:
            # Create error response
            error_msg = ChatMessage.objects.create(
                session=session,
                message_type='assistant',
                content="I'm sorry, I encountered an error while processing your message. Please try again.",
                response_type='error'
            )
            
            session.total_messages += 2
            session.save()
            
            return Response({
                'user_message': ChatMessageSerializer(user_msg).data,
                'assistant_message': ChatMessageSerializer(error_msg).data,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def rate_session(self, request, pk=None):
        """Rate the chat session quality"""
        session = get_object_or_404(ChatSession, pk=pk)
        rating = request.data.get('rating')
        
        if not rating or rating not in [1, 2, 3, 4, 5]:
            return Response(
                {'error': 'Rating must be between 1 and 5'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        analytics, created = session.analytics.get_or_create()
        analytics.user_satisfaction = rating
        analytics.save()
        
        return Response({'message': 'Rating saved successfully'})
    
    @action(detail=False)
    def active_sessions(self, request):
        """Get active chat sessions"""
        active_sessions = self.queryset.filter(is_active=True)[:10]
        serializer = ChatSessionSummarySerializer(active_sessions, many=True)
        return Response(serializer.data)
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


@method_decorator(csrf_exempt, name='dispatch')
class CommonQuestionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommonQuestions.objects.filter(is_active=True)
    serializer_class = CommonQuestionsSerializer
    
    @action(detail=False)
    def by_category(self, request):
        """Get questions grouped by category"""
        questions = self.queryset.order_by('category', '-times_asked')
        categories = {}
        
        for question in questions:
            if question.category not in categories:
                categories[question.category] = []
            categories[question.category].append(
                CommonQuestionsSerializer(question).data
            )
        
        return Response(categories)
    
    @action(detail=False)
    def popular(self, request):
        """Get most popular questions"""
        popular_questions = self.queryset.order_by('-times_asked')[:10]
        serializer = CommonQuestionsSerializer(popular_questions, many=True)
        return Response(serializer.data)