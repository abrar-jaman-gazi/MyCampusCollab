from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    is_suspended = models.BooleanField(default=False)
    profile_completed = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def display_name(self):
        return self.get_full_name() or self.username or self.email.split('@')[0]


class Skill(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    class Availability(models.TextChoices):
        AVAILABLE = 'available', 'Available for work'
        LIMITED = 'limited', 'Limited availability'
        UNAVAILABLE = 'unavailable', 'Not available'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile_images/', blank=True, validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])])
    cover = models.ImageField(upload_to='profile_covers/', blank=True, validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])])
    headline = models.CharField(max_length=160, blank=True)
    bio = models.TextField(blank=True)
    university = models.CharField(max_length=160, blank=True)
    department = models.CharField(max_length=160, blank=True)
    location = models.CharField(max_length=120, blank=True)
    availability = models.CharField(max_length=20, choices=Availability.choices, default=Availability.AVAILABLE)
    skills = models.ManyToManyField(Skill, blank=True, related_name='students')
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.display_name} profile'

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'username': self.user.username})

    @property
    def completion_percent(self):
        values = [self.user.first_name, self.user.last_name, self.avatar, self.headline, self.bio,
                  self.university, self.department, self.location, self.skills.exists()]
        return round(sum(bool(v) for v in values) / len(values) * 100)


class Education(models.Model):
    profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=180)
    degree = models.CharField(max_length=160)
    field = models.CharField(max_length=160, blank=True)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)
    current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_year']


class Experience(models.Model):
    profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='experience')
    title = models.CharField(max_length=160)
    organization = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']


class PortfolioItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=180)
    description = models.TextField()
    technologies = models.CharField(max_length=240, help_text='Comma-separated technologies')
    image = models.ImageField(upload_to='portfolios/', blank=True, validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])])
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    completed_on = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class SavedStudent(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_students')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_by_students')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['owner','student'], name='unique_saved_student')]
