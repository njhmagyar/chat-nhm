from django.contrib import admin
from .models import Project, Skill, Experience, PersonalInfo, Testimonial


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'client', 'featured', 'published', 'created_at']
    list_filter = ['category', 'featured', 'published', 'created_at']
    search_fields = ['title', 'description', 'client', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'category', 'tags')
        }),
        ('Media', {
            'fields': ('featured_image', 'gallery_images', 'video_url', 'prototype_url', 'live_url', 'github_url')
        }),
        ('Project Details', {
            'fields': ('client', 'role', 'duration', 'team_size')
        }),
        ('Case Study', {
            'fields': ('detailed_case_study', 'problem_statement', 'solution_overview', 'key_achievements', 'technologies_used')
        }),
        ('Settings', {
            'fields': ('featured', 'published')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'years_of_experience']
    list_filter = ['category', 'proficiency']
    search_fields = ['name', 'description']
    filter_horizontal = ['projects']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'experience_type', 'start_date', 'end_date', 'current']
    list_filter = ['experience_type', 'current', 'start_date']
    search_fields = ['title', 'organization', 'description']
    filter_horizontal = ['skills_gained']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'organization', 'location', 'experience_type')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'current')
        }),
        ('Details', {
            'fields': ('description', 'key_achievements', 'skills_gained')
        })
    )


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'location', 'years_of_experience']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'bio', 'location', 'email')
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'github_url', 'portfolio_url', 'behance_url', 'dribbble_url')
        }),
        ('Professional', {
            'fields': ('years_of_experience', 'availability_status')
        }),
        ('Personal', {
            'fields': ('fun_facts', 'design_philosophy', 'career_goals')
        })
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'author_company', 'rating', 'featured', 'created_at']
    list_filter = ['rating', 'featured', 'created_at']
    search_fields = ['author_name', 'author_company', 'content']
    
    fieldsets = (
        ('Author Information', {
            'fields': ('author_name', 'author_title', 'author_company', 'author_image')
        }),
        ('Testimonial', {
            'fields': ('content', 'rating', 'project')
        }),
        ('Settings', {
            'fields': ('featured',)
        })
    )