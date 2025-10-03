from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid


class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional user identification (for analytics)
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Session metadata
    total_messages = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Chat Session {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class ChatMessage(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('user', 'User Message'),
        ('assistant', 'Assistant Response'),
        ('system', 'System Message'),
    ]
    
    RESPONSE_TYPE_CHOICES = [
        ('text', 'Text Only'),
        ('text_with_media', 'Text with Media'),
        ('project_showcase', 'Project Showcase'),
        ('skill_summary', 'Skill Summary'),
        ('experience_timeline', 'Experience Timeline'),
        ('error', 'Error Response'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    
    # Message content
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES)
    content = models.TextField()
    response_type = models.CharField(max_length=30, choices=RESPONSE_TYPE_CHOICES, blank=True)
    
    # Metadata for responses
    referenced_projects = ArrayField(models.UUIDField(), blank=True, default=list)
    referenced_skills = ArrayField(models.IntegerField(), blank=True, default=list)
    referenced_experiences = ArrayField(models.IntegerField(), blank=True, default=list)
    
    # Media attachments
    media_urls = ArrayField(models.URLField(), blank=True, default=list)
    
    # RAG context
    retrieval_context = models.JSONField(blank=True, null=True)
    confidence_score = models.FloatField(null=True, blank=True)
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    response_time_ms = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.message_type.title()}: {self.content[:50]}..."


class ChatAnalytics(models.Model):
    """Track analytics for chat interactions"""
    
    session = models.OneToOneField(ChatSession, on_delete=models.CASCADE, related_name='analytics')
    
    # Conversation metrics
    conversation_length = models.IntegerField(default=0)
    avg_response_time = models.FloatField(default=0.0)
    user_satisfaction = models.IntegerField(null=True, blank=True)  # 1-5 rating
    
    # Content engagement
    projects_discussed = ArrayField(models.UUIDField(), blank=True, default=list)
    skills_mentioned = ArrayField(models.IntegerField(), blank=True, default=list)
    most_asked_topics = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    
    # Technical metrics
    total_tokens_used = models.IntegerField(default=0)
    retrieval_accuracy = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analytics for {self.session}"


class CommonQuestions(models.Model):
    """Store frequently asked questions for quick responses"""
    
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=100)
    
    # Usage tracking
    times_asked = models.IntegerField(default=0)
    last_asked = models.DateTimeField(auto_now=True)
    
    # Content references
    related_projects = models.ManyToManyField('content.Project', blank=True)
    related_skills = models.ManyToManyField('content.Skill', blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-times_asked', 'category']
    
    def __str__(self):
        return f"FAQ: {self.question[:50]}..."