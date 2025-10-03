from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .chat_service import ChatService
from .embedding_service import EmbeddingService


class SuggestedQuestionsView(APIView):
    """Get suggested questions for the chat interface"""
    
    def get(self, request):
        chat_service = ChatService()
        questions = chat_service.get_suggested_questions()
        return Response({'questions': questions})


class TestRetrievalView(APIView):
    """Test the RAG retrieval system"""
    
    def post(self, request):
        query = request.data.get('query')
        if not query:
            return Response(
                {'error': 'Query is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        embedding_service = EmbeddingService()
        results = embedding_service.similarity_search(query, top_k=5)
        
        formatted_results = []
        for content_embedding, similarity_score in results:
            content_data = embedding_service.get_content_by_embedding(content_embedding)
            formatted_results.append({
                'content_type': content_embedding.content_type,
                'content_id': content_embedding.content_id,
                'similarity_score': similarity_score,
                'content_preview': content_embedding.content_text[:200] + '...',
                'content_data': content_data
            })
        
        return Response({
            'query': query,
            'results': formatted_results,
            'total_results': len(results)
        })