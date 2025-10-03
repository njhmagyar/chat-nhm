from django.db import models


class ContentEmbedding(models.Model):
    """Store pre-computed embeddings for content pieces"""
    
    CONTENT_TYPE_CHOICES = [
        ('project', 'Project'),
        ('skill', 'Skill'),
        ('experience', 'Experience'),
        ('personal_info', 'Personal Info'),
        ('testimonial', 'Testimonial'),
        ('faq', 'FAQ'),
    ]
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    content_id = models.CharField(max_length=100)  # UUID or ID as string
    content_text = models.TextField()
    
    # Store embedding as JSON for flexibility
    embedding_vector = models.JSONField()
    embedding_model = models.CharField(max_length=100, default='text-embedding-3-small')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['content_type', 'content_id']
        indexes = [
            models.Index(fields=['content_type']),
            models.Index(fields=['content_id']),
        ]
    
    def __str__(self):
        return f"{self.content_type}:{self.content_id}"


class RetrievalLog(models.Model):
    """Log retrieval requests for analysis and improvement"""
    
    query = models.TextField()
    query_embedding = models.JSONField()
    
    # Results
    retrieved_content_ids = models.JSONField()  # List of content IDs
    similarity_scores = models.JSONField()  # Corresponding similarity scores
    
    # Context
    session_id = models.UUIDField(null=True, blank=True)
    response_generated = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Query: {self.query[:50]}..."