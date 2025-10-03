from django.contrib import admin
from .models import ChatSession, ChatMessage, ChatAnalytics, CommonQuestions


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_name', 'total_messages', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['id', 'session_name', 'user_ip']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Session Info', {
            'fields': ('id', 'session_name', 'is_active')
        }),
        ('User Info', {
            'fields': ('user_ip', 'user_agent')
        }),
        ('Statistics', {
            'fields': ('total_messages', 'created_at', 'updated_at')
        })
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'response_type', 'created_at']
    list_filter = ['message_type', 'response_type', 'created_at']
    search_fields = ['content', 'session__id']
    readonly_fields = ['id', 'created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    fieldsets = (
        ('Message Info', {
            'fields': ('session', 'message_type', 'content', 'response_type')
        }),
        ('References', {
            'fields': ('referenced_projects', 'referenced_skills', 'referenced_experiences', 'media_urls')
        }),
        ('Technical', {
            'fields': ('retrieval_context', 'confidence_score', 'response_time_ms')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at')
        })
    )


@admin.register(ChatAnalytics)
class ChatAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['session', 'conversation_length', 'avg_response_time', 'user_satisfaction', 'created_at']
    list_filter = ['user_satisfaction', 'created_at']
    readonly_fields = ['created_at']


@admin.register(CommonQuestions)
class CommonQuestionsAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'category', 'times_asked', 'is_active', 'last_asked']
    list_filter = ['category', 'is_active', 'last_asked']
    search_fields = ['question', 'answer', 'category']
    filter_horizontal = ['related_projects', 'related_skills']
    
    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'
    
    fieldsets = (
        ('Question & Answer', {
            'fields': ('question', 'answer', 'category')
        }),
        ('Usage Stats', {
            'fields': ('times_asked', 'is_active')
        }),
        ('Related Content', {
            'fields': ('related_projects', 'related_skills')
        })
    )