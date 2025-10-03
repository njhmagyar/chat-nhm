import openai
from django.conf import settings

# Apply OpenAI client fix
from .openai_fix import fixed_openai_init
from typing import List, Tuple, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging

from content.models import Project, Skill, Experience, PersonalInfo, Testimonial
from .models import ContentEmbedding, RetrievalLog

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating and managing content embeddings"""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            logger.warning("No OpenAI API key provided. Embedding service will not work.")
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dimension = 1536
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a given text"""
        if not self.client:
            logger.error("OpenAI client not initialized. Check your API key.")
            return []
        
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []
    
    def embed_project(self, project: Project) -> str:
        """Generate and store embedding for a project"""
        # Combine all relevant project text
        content_text = f"""
        Title: {project.title}
        Description: {project.description}
        Category: {project.get_category_display()}
        Role: {project.role}
        Client: {project.client}
        Problem: {project.problem_statement}
        Solution: {project.solution_overview}
        Case Study: {project.detailed_case_study}
        Technologies: {', '.join(project.technologies_used)}
        Tags: {', '.join(project.tags)}
        Achievements: {' '.join(project.key_achievements)}
        """.strip()
        
        embedding = self.generate_embedding(content_text)
        if embedding:
            ContentEmbedding.objects.update_or_create(
                content_type='project',
                content_id=str(project.id),
                defaults={
                    'content_text': content_text,
                    'embedding_vector': embedding,
                    'embedding_model': self.embedding_model
                }
            )
            return str(project.id)
        return None
    
    def embed_skill(self, skill: Skill) -> str:
        """Generate and store embedding for a skill"""
        content_text = f"""
        Skill: {skill.name}
        Category: {skill.get_category_display()}
        Proficiency: {skill.get_proficiency_display()}
        Experience: {skill.years_of_experience} years
        Description: {skill.description}
        """.strip()
        
        embedding = self.generate_embedding(content_text)
        if embedding:
            ContentEmbedding.objects.update_or_create(
                content_type='skill',
                content_id=str(skill.id),
                defaults={
                    'content_text': content_text,
                    'embedding_vector': embedding,
                    'embedding_model': self.embedding_model
                }
            )
            return str(skill.id)
        return None
    
    def embed_experience(self, experience: Experience) -> str:
        """Generate and store embedding for an experience"""
        content_text = f"""
        Title: {experience.title}
        Organization: {experience.organization}
        Type: {experience.get_experience_type_display()}
        Location: {experience.location}
        Duration: {experience.start_date} to {experience.end_date or 'Present'}
        Description: {experience.description}
        Achievements: {' '.join(experience.key_achievements)}
        """.strip()
        
        embedding = self.generate_embedding(content_text)
        if embedding:
            ContentEmbedding.objects.update_or_create(
                content_type='experience',
                content_id=str(experience.id),
                defaults={
                    'content_text': content_text,
                    'embedding_vector': embedding,
                    'embedding_model': self.embedding_model
                }
            )
            return str(experience.id)
        return None
    
    def embed_personal_info(self, personal_info: PersonalInfo) -> str:
        """Generate and store embedding for personal information"""
        content_text = f"""
        Name: {personal_info.name}
        Title: {personal_info.title}
        Bio: {personal_info.bio}
        Location: {personal_info.location}
        Experience: {personal_info.years_of_experience} years
        Availability: {personal_info.availability_status}
        Design Philosophy: {personal_info.design_philosophy}
        Career Goals: {personal_info.career_goals}
        Fun Facts: {' '.join(personal_info.fun_facts)}
        """.strip()
        
        embedding = self.generate_embedding(content_text)
        if embedding:
            ContentEmbedding.objects.update_or_create(
                content_type='personal_info',
                content_id=str(personal_info.id),
                defaults={
                    'content_text': content_text,
                    'embedding_vector': embedding,
                    'embedding_model': self.embedding_model
                }
            )
            return str(personal_info.id)
        return None
    
    def embed_testimonial(self, testimonial: Testimonial) -> str:
        """Generate and store embedding for a testimonial"""
        content_text = f"""
        Testimonial from {testimonial.author_name}, {testimonial.author_title} at {testimonial.author_company}:
        {testimonial.content}
        Rating: {testimonial.rating}/5 stars
        """.strip()
        
        embedding = self.generate_embedding(content_text)
        if embedding:
            ContentEmbedding.objects.update_or_create(
                content_type='testimonial',
                content_id=str(testimonial.id),
                defaults={
                    'content_text': content_text,
                    'embedding_vector': embedding,
                    'embedding_model': self.embedding_model
                }
            )
            return str(testimonial.id)
        return None
    
    def embed_all_content(self):
        """Generate embeddings for all portfolio content"""
        logger.info("Starting to embed all content...")
        
        # Embed projects
        for project in Project.objects.filter(published=True):
            self.embed_project(project)
            logger.info(f"Embedded project: {project.title}")
        
        # Embed skills
        for skill in Skill.objects.all():
            self.embed_skill(skill)
            logger.info(f"Embedded skill: {skill.name}")
        
        # Embed experiences
        for experience in Experience.objects.all():
            self.embed_experience(experience)
            logger.info(f"Embedded experience: {experience.title}")
        
        # Embed personal info
        for personal_info in PersonalInfo.objects.all():
            self.embed_personal_info(personal_info)
            logger.info(f"Embedded personal info for: {personal_info.name}")
        
        # Embed testimonials
        for testimonial in Testimonial.objects.all():
            self.embed_testimonial(testimonial)
            logger.info(f"Embedded testimonial from: {testimonial.author_name}")
        
        logger.info("Finished embedding all content")
    
    def similarity_search(self, query: str, top_k: int = 5) -> List[Tuple[ContentEmbedding, float]]:
        """Perform similarity search for a query"""
        query_embedding = self.generate_embedding(query)
        if not query_embedding:
            return []
        
        # Get all embeddings
        all_embeddings = ContentEmbedding.objects.all()
        
        if not all_embeddings:
            return []
        
        # Calculate similarities
        results = []
        for content_embedding in all_embeddings:
            if content_embedding.embedding_vector:
                similarity = cosine_similarity(
                    [query_embedding],
                    [content_embedding.embedding_vector]
                )[0][0]
                results.append((content_embedding, similarity))
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Log the retrieval
        RetrievalLog.objects.create(
            query=query,
            query_embedding=query_embedding,
            retrieved_content_ids=[result[0].content_id for result in results[:top_k]],
            similarity_scores=[result[1] for result in results[:top_k]]
        )
        
        return results[:top_k]
    
    def get_content_by_embedding(self, content_embedding: ContentEmbedding) -> Dict[str, Any]:
        """Retrieve the actual content object from ContentEmbedding"""
        content_type = content_embedding.content_type
        content_id = content_embedding.content_id
        
        try:
            if content_type == 'project':
                obj = Project.objects.get(id=content_id)
                return {
                    'type': 'project',
                    'object': obj,
                    'title': obj.title,
                    'description': obj.description,
                    'featured_image': obj.featured_image,
                    'gallery_images': obj.gallery_images,
                    'video_url': obj.video_url,
                    'prototype_url': obj.prototype_url,
                    'live_url': obj.live_url
                }
            elif content_type == 'skill':
                obj = Skill.objects.get(id=content_id)
                return {
                    'type': 'skill',
                    'object': obj,
                    'name': obj.name,
                    'proficiency': obj.proficiency,
                    'description': obj.description
                }
            elif content_type == 'experience':
                obj = Experience.objects.get(id=content_id)
                return {
                    'type': 'experience',
                    'object': obj,
                    'title': obj.title,
                    'organization': obj.organization,
                    'description': obj.description
                }
            elif content_type == 'personal_info':
                obj = PersonalInfo.objects.get(id=content_id)
                return {
                    'type': 'personal_info',
                    'object': obj,
                    'name': obj.name,
                    'bio': obj.bio,
                    'title': obj.title
                }
            elif content_type == 'testimonial':
                obj = Testimonial.objects.get(id=content_id)
                return {
                    'type': 'testimonial',
                    'object': obj,
                    'author_name': obj.author_name,
                    'content': obj.content,
                    'rating': obj.rating
                }
        except Exception as e:
            logger.error(f"Error retrieving content {content_type}:{content_id}: {e}")
        
        return None