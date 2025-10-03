from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Design'),
        ('mobile', 'Mobile App'),
        ('ux', 'UX Research'),
        ('branding', 'Branding'),
        ('prototype', 'Prototype'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    detailed_case_study = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tags = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    
    # Media fields
    featured_image = models.URLField(blank=True)
    gallery_images = ArrayField(models.URLField(), blank=True, default=list)
    video_url = models.URLField(blank=True)
    prototype_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Project details
    client = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    team_size = models.IntegerField(default=1)
    
    # Project metadata
    problem_statement = models.TextField(blank=True)
    solution_overview = models.TextField(blank=True)
    key_achievements = ArrayField(models.TextField(), blank=True, default=list)
    technologies_used = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    
    # SEO and discovery
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Vector embedding for RAG
    embedding = ArrayField(models.FloatField(), size=1536, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('design', 'Design Tools'),
        ('research', 'Research Methods'),
        ('technical', 'Technical Skills'),
        ('soft', 'Soft Skills'),
        ('process', 'Process & Methods'),
    ]
    
    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)
    years_of_experience = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    projects = models.ManyToManyField(Project, blank=True, related_name='skills_used')
    
    # Vector embedding for RAG
    embedding = ArrayField(models.FloatField(), size=1536, blank=True, null=True)
    
    class Meta:
        ordering = ['category', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.proficiency})"


class Experience(models.Model):
    EXPERIENCE_TYPE_CHOICES = [
        ('work', 'Work Experience'),
        ('education', 'Education'),
        ('volunteer', 'Volunteer'),
        ('freelance', 'Freelance'),
        ('personal', 'Personal Project'),
    ]
    
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPE_CHOICES)
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    
    description = models.TextField()
    key_achievements = ArrayField(models.TextField(), blank=True, default=list)
    skills_gained = models.ManyToManyField(Skill, blank=True, related_name='experiences')
    
    # Vector embedding for RAG
    embedding = ArrayField(models.FloatField(), size=1536, blank=True, null=True)
    
    class Meta:
        ordering = ['-start_date']
        
    def __str__(self):
        return f"{self.title} at {self.organization}"


class PersonalInfo(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    location = models.CharField(max_length=100)
    email = models.EmailField()
    
    # Social links
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    behance_url = models.URLField(blank=True)
    dribbble_url = models.URLField(blank=True)
    
    # Professional info
    years_of_experience = models.IntegerField(default=0)
    availability_status = models.CharField(max_length=100, default='Open to opportunities')
    
    # Personal touches
    fun_facts = ArrayField(models.TextField(), blank=True, default=list)
    design_philosophy = models.TextField(blank=True)
    career_goals = models.TextField(blank=True)
    
    # Vector embedding for RAG
    embedding = ArrayField(models.FloatField(), size=1536, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Personal Information'
        verbose_name_plural = 'Personal Information'


class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=200)
    author_company = models.CharField(max_length=100, blank=True)
    author_image = models.URLField(blank=True)
    
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='testimonials')
    
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Vector embedding for RAG
    embedding = ArrayField(models.FloatField(), size=1536, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Testimonial from {self.author_name}"