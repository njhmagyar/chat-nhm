"""Fallback chat service that works without OpenAI"""

import logging
from typing import Dict, List, Any
from .embedding_service_fallback import EmbeddingService
from content.models import Project, Skill, Experience, PersonalInfo

logger = logging.getLogger(__name__)


class ChatService:
    """Fallback service for generating responses without OpenAI"""
    
    def __init__(self):
        logger.info("Using fallback chat service (no OpenAI required)")
        self.embedding_service = EmbeddingService()
        self.model = "fallback"
    
    def generate_response(self, user_message: str, session_id: str = None) -> Dict[str, Any]:
        """Generate a response using simple rule-based logic"""
        
        # Step 1: Search for relevant content
        relevant_content = self.embedding_service.similarity_search(user_message, top_k=5)
        
        # Step 2: Generate a simple response
        response_content = self._generate_fallback_response(user_message, relevant_content)
        
        # Step 3: Enhance response with media and references
        enhanced_response = self._enhance_response(response_content, relevant_content)
        
        return enhanced_response
    
    def _generate_fallback_response(self, user_message: str, relevant_content: List[tuple]) -> str:
        """Generate a simple rule-based response"""
        user_lower = user_message.lower()
        
        # Get personal info for context
        try:
            personal_info = PersonalInfo.objects.first()
            name = personal_info.name if personal_info else "the designer"
        except:
            name = "the designer"
        
        # Simple keyword-based responses
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            return f"Hello! I'm here to help you learn about {name}'s work and experience. What would you like to know?"
        
        elif any(word in user_lower for word in ['project', 'work', 'portfolio']):
            if relevant_content:
                return f"I found some relevant projects for you! {name} has worked on various design projects including web design, mobile apps, and user experience research. You can see some examples below."
            else:
                return f"{name} has worked on many exciting projects. Let me know if you'd like to hear about specific types of work!"
        
        elif any(word in user_lower for word in ['skill', 'technology', 'tool']):
            return f"{name} has experience with various design tools and technologies. This includes both technical skills and creative abilities across different design disciplines."
        
        elif any(word in user_lower for word in ['experience', 'background', 'career']):
            return f"I'd be happy to tell you about {name}'s professional background and career journey. They have experience in design and development across various industries."
        
        elif any(word in user_lower for word in ['contact', 'hire', 'available']):
            if personal_info and personal_info.availability_status:
                return f"{name} is currently {personal_info.availability_status.lower()}. Feel free to reach out to discuss potential opportunities!"
            else:
                return f"You can contact {name} to discuss potential projects and collaborations."
        
        else:
            # Generic response when we have relevant content
            if relevant_content:
                return f"I found some information related to your question about {name}'s work. Let me share what I know!"
            else:
                return f"That's an interesting question! While I don't have specific information about that topic, I'd be happy to tell you about {name}'s projects, skills, or experience. What would you like to know more about?"
    
    def _enhance_response(self, content: str, relevant_content: List[tuple]) -> Dict[str, Any]:
        """Enhance response with references to actual content"""
        
        referenced_projects = []
        referenced_skills = []
        referenced_experiences = []
        media_urls = []
        
        # Extract references from relevant content
        for content_embedding, similarity_score in relevant_content[:3]:  # Top 3 results
            content_data = self.embedding_service.get_content_by_embedding(content_embedding)
            if not content_data:
                continue
            
            content_type = content_data['type']
            obj = content_data['object']
            
            if content_type == 'project':
                referenced_projects.append(str(obj.id))
                # Add media URLs
                if obj.featured_image:
                    media_urls.append(obj.featured_image)
                if obj.gallery_images:
                    media_urls.extend(obj.gallery_images[:2])  # Limit to 2 images
            
            elif content_type == 'skill':
                referenced_skills.append(obj.id)
            
            elif content_type == 'experience':
                referenced_experiences.append(obj.id)
        
        # Determine response type
        response_type = 'text'
        if referenced_projects and media_urls:
            response_type = 'project_showcase'
        elif referenced_projects:
            response_type = 'text_with_media'
        elif referenced_skills:
            response_type = 'skill_summary'
        elif referenced_experiences:
            response_type = 'experience_timeline'
        
        return {
            'content': content,
            'response_type': response_type,
            'referenced_projects': referenced_projects,
            'referenced_skills': referenced_skills,
            'referenced_experiences': referenced_experiences,
            'media_urls': media_urls,
            'confidence_score': 0.8 if relevant_content else 0.3,
            'retrieval_context': {
                'query_matches': len(relevant_content),
                'high_confidence_matches': len([score for _, score in relevant_content if score > 0.5])
            },
            'tokens_used': 0  # No tokens used in fallback
        }
    
    def get_suggested_questions(self) -> List[str]:
        """Get suggested questions for users"""
        return [
            "What kind of design projects have you worked on?",
            "Tell me about your design process",
            "What tools and technologies do you use?",
            "Can you show me some of your recent work?",
            "What's your experience with user research?",
            "How do you approach problem-solving in design?",
            "What are you passionate about in design?",
            "Tell me about your background and experience",
            "What's your design philosophy?",
            "Are you available for new projects?"
        ]