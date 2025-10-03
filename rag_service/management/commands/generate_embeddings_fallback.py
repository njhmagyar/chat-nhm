from django.core.management.base import BaseCommand
from rag_service.embedding_service_fallback import EmbeddingService


class Command(BaseCommand):
    help = 'Generate fallback embeddings without OpenAI'
    
    def handle(self, *args, **options):
        self.stdout.write('Generating fallback embeddings (no OpenAI required)...')
        
        embedding_service = EmbeddingService()
        embedding_service.embed_all_content()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully generated fallback embeddings!')
        )