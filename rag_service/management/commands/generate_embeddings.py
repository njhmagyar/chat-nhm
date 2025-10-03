from django.core.management.base import BaseCommand
from rag_service.embedding_service import EmbeddingService


class Command(BaseCommand):
    help = 'Generate embeddings for all portfolio content'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--content-type',
            type=str,
            help='Generate embeddings for specific content type (project, skill, experience, personal_info, testimonial)',
        )
    
    def handle(self, *args, **options):
        embedding_service = EmbeddingService()
        
        content_type = options.get('content_type')
        
        if content_type:
            self.stdout.write(f'Generating embeddings for {content_type}...')
            
            if content_type == 'project':
                from content.models import Project
                for project in Project.objects.filter(published=True):
                    embedding_service.embed_project(project)
                    self.stdout.write(f'✓ Embedded project: {project.title}')
            
            elif content_type == 'skill':
                from content.models import Skill
                for skill in Skill.objects.all():
                    embedding_service.embed_skill(skill)
                    self.stdout.write(f'✓ Embedded skill: {skill.name}')
            
            elif content_type == 'experience':
                from content.models import Experience
                for experience in Experience.objects.all():
                    embedding_service.embed_experience(experience)
                    self.stdout.write(f'✓ Embedded experience: {experience.title}')
            
            elif content_type == 'personal_info':
                from content.models import PersonalInfo
                for personal_info in PersonalInfo.objects.all():
                    embedding_service.embed_personal_info(personal_info)
                    self.stdout.write(f'✓ Embedded personal info: {personal_info.name}')
            
            elif content_type == 'testimonial':
                from content.models import Testimonial
                for testimonial in Testimonial.objects.all():
                    embedding_service.embed_testimonial(testimonial)
                    self.stdout.write(f'✓ Embedded testimonial: {testimonial.author_name}')
            
            else:
                self.stdout.write(
                    self.style.ERROR(f'Unknown content type: {content_type}')
                )
                return
        
        else:
            self.stdout.write('Generating embeddings for all content...')
            embedding_service.embed_all_content()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully generated embeddings!')
        )