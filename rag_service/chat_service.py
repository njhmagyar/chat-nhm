import openai
from django.conf import settings

# Apply OpenAI client fix
from .openai_fix import fixed_openai_init
from typing import Dict, List, Any
import json
import logging

from .embedding_service import EmbeddingService
from content.models import Project, Skill, Experience, PersonalInfo

logger = logging.getLogger(__name__)


class ChatService:
    """Service for generating conversational responses using RAG"""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            logger.warning("No OpenAI API key provided. Chat service will not work.")
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.embedding_service = EmbeddingService()
        self.model = "gpt-4o-mini"
    
    def generate_response(self, user_message: str, session_id: str = None) -> Dict[str, Any]:
        """Generate a conversational response using RAG"""
        
        # Step 1: Retrieve relevant content
        relevant_content = self.embedding_service.similarity_search(user_message, top_k=5)
        
        # Step 2: Build context from retrieved content
        context = self._build_context(relevant_content)
        
        # Step 3: Generate response using LLM
        response_data = self._generate_llm_response(user_message, context)
        
        # Step 4: Enhance response with media and references
        enhanced_response = self._enhance_response(response_data, relevant_content)
        
        return enhanced_response
    
    def _build_context(self, relevant_content: List[tuple]) -> str:
        """Build context string from retrieved content"""
        context_parts = []
        
        for content_embedding, similarity_score in relevant_content:
            if similarity_score < 0.3:  # Skip low-relevance content
                continue
            
            content_data = self.embedding_service.get_content_by_embedding(content_embedding)
            if content_data:
                context_parts.append(self._format_content_for_context(content_data))
        
        return "\n\n".join(context_parts)
    
    def _format_content_for_context(self, content_data: Dict[str, Any]) -> str:
        """Format content data for use in LLM context"""
        content_type = content_data['type']
        obj = content_data['object']
        
        if content_type == 'project':
            return f"""
PROJECT: {obj.title}
Category: {obj.category}
Role: {obj.role}
Client: {obj.client}
Description: {obj.description}
Problem: {obj.problem_statement}
Solution: {obj.solution_overview}
Technologies: {', '.join(obj.technologies_used)}
Key Achievements: {' '.join(obj.key_achievements)}
Live URL: {obj.live_url}
GitHub: {obj.github_url}
Featured Image: {obj.featured_image}
Gallery Images: {obj.gallery_images}
Video: {obj.video_url}
Prototype: {obj.prototype_url}
            """.strip()
        
        elif content_type == 'skill':
            return f"""
SKILL: {obj.name}
Category: {obj.get_category_display()}
Proficiency: {obj.get_proficiency_display()}
Years of Experience: {obj.years_of_experience}
Description: {obj.description}
            """.strip()
        
        elif content_type == 'experience':
            return f"""
EXPERIENCE: {obj.title} at {obj.organization}
Type: {obj.get_experience_type_display()}
Duration: {obj.start_date} to {obj.end_date or 'Present'}
Location: {obj.location}
Description: {obj.description}
Key Achievements: {' '.join(obj.key_achievements)}
            """.strip()
        
        elif content_type == 'personal_info':
            return f"""
PERSONAL INFO:
Name: {obj.name}
Title: {obj.title}
Bio: {obj.bio}
Location: {obj.location}
Years of Experience: {obj.years_of_experience}
Availability: {obj.availability_status}
Design Philosophy: {obj.design_philosophy}
Career Goals: {obj.career_goals}
Fun Facts: {' '.join(obj.fun_facts)}
LinkedIn: {obj.linkedin_url}
GitHub: {obj.github_url}
Portfolio: {obj.portfolio_url}
            """.strip()
        
        elif content_type == 'testimonial':
            return f"""
TESTIMONIAL from {obj.author_name} ({obj.author_title} at {obj.author_company}):
"{obj.content}"
Rating: {obj.rating}/5 stars
            """.strip()
        
        return ""
    
    def _generate_llm_response(self, user_message: str, context: str) -> Dict[str, Any]:
        """Generate response using OpenAI's API"""
        
        system_prompt = f"""
You are a conversational AI assistant representing a product designer's portfolio. Your role is to help visitors learn about the designer's work, skills, experience, and design philosophy in a natural, engaging way.

PERSONALITY:
- Professional but friendly and approachable
- Enthusiastic about design and problem-solving
- Confident but humble about achievements
- Use first person ("I", "my") when discussing the designer's work
- Be conversational, not robotic or overly formal

GUIDELINES:
- Answer questions based ONLY on the provided context
- If you don't have information, say so honestly and suggest what you can help with instead
- When discussing projects, highlight the design process, challenges, and outcomes
- Be specific about technologies, tools, and methodologies when relevant
- Offer to show or explain more details when appropriate
- Keep responses focused and not overly long unless asked for detailed explanations

CONTEXT ABOUT THE DESIGNER:
{context}

Remember: You are speaking AS the designer, so use first person when appropriate. Be helpful, informative, and engaging while staying true to the provided information.
        """
        
        if not self.client:
            return {
                'content': "I'm sorry, the chat service is not properly configured. Please check the OpenAI API key.",
                'error': 'No OpenAI client available'
            }
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            return {
                'content': content,
                'tokens_used': response.usage.total_tokens,
                'model': self.model
            }
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return {
                'content': "I'm sorry, I'm having trouble processing your question right now. Could you please try rephrasing it?",
                'error': str(e)
            }
    
    def _enhance_response(self, response_data: Dict[str, Any], relevant_content: List[tuple]) -> Dict[str, Any]:
        """Enhance response with media URLs and references"""
        
        if 'error' in response_data:
            return {
                'content': response_data['content'],
                'response_type': 'error',
                'confidence_score': 0.0
            }
        
        # Extract referenced content
        referenced_projects = []
        referenced_skills = []
        referenced_experiences = []
        media_urls = []
        
        for content_embedding, similarity_score in relevant_content:
            if similarity_score < 0.4:  # Only include high-relevance content
                continue
            
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
                    media_urls.extend(obj.gallery_images[:3])  # Limit to 3 images
                if obj.video_url:
                    media_urls.append(obj.video_url)
            
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
        
        # Calculate confidence score
        confidence_score = 0.0
        if relevant_content:
            confidence_score = max(score for _, score in relevant_content)
        
        return {
            'content': response_data['content'],
            'response_type': response_type,
            'referenced_projects': referenced_projects,
            'referenced_skills': referenced_skills,
            'referenced_experiences': referenced_experiences,
            'media_urls': media_urls,
            'confidence_score': confidence_score,
            'retrieval_context': {
                'query_matches': len(relevant_content),
                'high_confidence_matches': len([score for _, score in relevant_content if score > 0.5])
            },
            'tokens_used': response_data.get('tokens_used', 0)
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