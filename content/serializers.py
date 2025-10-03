from rest_framework import serializers
from .models import Project, Skill, Experience, PersonalInfo, Testimonial


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'detailed_case_study', 
            'category', 'tags', 'featured_image', 'gallery_images', 
            'video_url', 'prototype_url', 'live_url', 'github_url',
            'client', 'role', 'duration', 'team_size', 'problem_statement',
            'solution_overview', 'key_achievements', 'technologies_used',
            'featured', 'published', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProjectSummarySerializer(serializers.ModelSerializer):
    """Lighter serializer for project listings"""
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'category', 'tags',
            'featured_image', 'client', 'role', 'featured', 'created_at'
        ]


class SkillSerializer(serializers.ModelSerializer):
    projects_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'category', 'proficiency', 'years_of_experience',
            'description', 'projects_count'
        ]
    
    def get_projects_count(self, obj):
        return obj.projects.filter(published=True).count()


class ExperienceSerializer(serializers.ModelSerializer):
    skills_gained = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Experience
        fields = [
            'id', 'title', 'organization', 'location', 'experience_type',
            'start_date', 'end_date', 'current', 'description',
            'key_achievements', 'skills_gained'
        ]


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = [
            'name', 'title', 'bio', 'location', 'email', 'linkedin_url',
            'github_url', 'portfolio_url', 'behance_url', 'dribbble_url',
            'years_of_experience', 'availability_status', 'fun_facts',
            'design_philosophy', 'career_goals'
        ]


class TestimonialSerializer(serializers.ModelSerializer):
    project = ProjectSummarySerializer(read_only=True)
    
    class Meta:
        model = Testimonial
        fields = [
            'id', 'author_name', 'author_title', 'author_company',
            'author_image', 'content', 'rating', 'project', 'created_at'
        ]