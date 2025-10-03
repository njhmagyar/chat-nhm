from rest_framework import serializers
from .models import ChatSession, ChatMessage, ChatAnalytics, CommonQuestions


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'message_type', 'content', 'response_type',
            'referenced_projects', 'referenced_skills', 'referenced_experiences',
            'media_urls', 'confidence_score', 'created_at', 'response_time_ms'
        ]
        read_only_fields = ['id', 'created_at', 'response_time_ms', 'confidence_score']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = [
            'id', 'session_name', 'created_at', 'updated_at',
            'total_messages', 'is_active', 'messages', 'message_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_messages']
    
    def get_message_count(self, obj):
        return obj.messages.count()


class ChatSessionSummarySerializer(serializers.ModelSerializer):
    """Lighter serializer for session lists"""
    last_message_time = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = [
            'id', 'session_name', 'created_at', 'total_messages',
            'is_active', 'last_message_time'
        ]
    
    def get_last_message_time(self, obj):
        last_message = obj.messages.last()
        return last_message.created_at if last_message else obj.created_at


class SendMessageSerializer(serializers.Serializer):
    """Serializer for sending new messages"""
    message = serializers.CharField(max_length=5000)
    session_id = serializers.UUIDField(required=False)
    
    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        return value.strip()


class CommonQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonQuestions
        fields = [
            'id', 'question', 'answer', 'category', 'times_asked'
        ]


class ChatAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatAnalytics
        fields = [
            'conversation_length', 'avg_response_time', 'user_satisfaction',
            'projects_discussed', 'skills_mentioned', 'most_asked_topics',
            'total_tokens_used', 'retrieval_accuracy'
        ]