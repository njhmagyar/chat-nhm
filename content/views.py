from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Skill, Experience, PersonalInfo, Testimonial
from .serializers import (
    ProjectSerializer, ProjectSummarySerializer, SkillSerializer,
    ExperienceSerializer, PersonalInfoSerializer, TestimonialSerializer
)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(published=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'featured']
    search_fields = ['title', 'description', 'tags', 'technologies_used']
    ordering_fields = ['created_at', 'title']
    ordering = ['-featured', '-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectSummarySerializer
        return ProjectSerializer
    
    @action(detail=False)
    def featured(self, request):
        """Get featured projects"""
        featured_projects = self.queryset.filter(featured=True)
        serializer = ProjectSummarySerializer(featured_projects, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def categories(self, request):
        """Get all available categories"""
        categories = Project.CATEGORY_CHOICES
        return Response([{'value': value, 'label': label} for value, label in categories])


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'proficiency']
    search_fields = ['name', 'description']
    
    @action(detail=False)
    def by_category(self, request):
        """Get skills grouped by category"""
        skills_by_category = {}
        for category_value, category_label in Skill.CATEGORY_CHOICES:
            skills = self.queryset.filter(category=category_value)
            skills_by_category[category_value] = {
                'label': category_label,
                'skills': SkillSerializer(skills, many=True).data
            }
        return Response(skills_by_category)


class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['experience_type', 'current']
    ordering = ['-start_date']


class PersonalInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PersonalInfo.objects.all()
    serializer_class = PersonalInfoSerializer
    
    @action(detail=False)
    def profile(self, request):
        """Get the main personal profile"""
        try:
            profile = PersonalInfo.objects.first()
            if profile:
                serializer = PersonalInfoSerializer(profile)
                return Response(serializer.data)
            return Response({'error': 'Profile not found'}, status=404)
        except PersonalInfo.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['featured', 'rating']
    ordering = ['-created_at']
    
    @action(detail=False)
    def featured(self, request):
        """Get featured testimonials"""
        featured_testimonials = self.queryset.filter(featured=True)
        serializer = TestimonialSerializer(featured_testimonials, many=True)
        return Response(serializer.data)