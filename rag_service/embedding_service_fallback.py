"""Fallback embedding service that works without OpenAI"""

import logging
from typing import List, Tuple, Dict, Any
from content.models import Project, Skill, Experience, PersonalInfo, Testimonial
from .models import ContentEmbedding, RetrievalLog

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Fallback service that uses simple text matching instead of embeddings"""
    
    def __init__(self):
        logger.info("Using fallback embedding service (no OpenAI required)")
        self.embedding_model = "fallback"
        self.embedding_dimension = 1536
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate a simple hash-based 'embedding'"""
        # Simple hash-based embedding for testing
        import hashlib
        hash_obj = hashlib.md5(text.lower().encode())
        # Convert to list of floats (not a real embedding, but works for testing)
        return [float(ord(c)) for c in hash_obj.hexdigest()[:32]]
    
    def similarity_search(self, query: str, top_k: int = 5) -> List[Tuple[ContentEmbedding, float]]:
        """Simple text-based search fallback"""
        query_lower = query.lower()
        results = []
        
        # Get all content and do simple text matching
        all_embeddings = ContentEmbedding.objects.all()
        
        for content_embedding in all_embeddings:
            # Simple text similarity (contains check)
            content_lower = content_embedding.content_text.lower()
            
            # Count matching words
            query_words = set(query_lower.split())
            content_words = set(content_lower.split())
            common_words = query_words.intersection(content_words)
            
            if common_words:
                similarity = len(common_words) / max(len(query_words), 1)
                results.append((content_embedding, similarity))
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def embed_all_content(self):
        """Store basic content information without real embeddings"""
        logger.info("Creating fallback content entries...")
        
        # Just store the content text without real embeddings
        for project in Project.objects.filter(published=True):
            content_text = f"{project.title} {project.description} {project.role}"
            ContentEmbedding.objects.update_or_create(
                content_type='project',
                content_id=str(project.id),
                defaults={
                    'content_text': content_text,
                    'embedding_vector': [],  # Empty for fallback
                    'embedding_model': self.embedding_model
                }
            )
        
        logger.info("Fallback content storage complete")