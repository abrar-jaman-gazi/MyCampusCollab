from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from apps.accounts.models import Skill


class GigCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True)
    icon = models.CharField(max_length=50, default='briefcase')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Gig categories'
        ordering = ['name']

    def __str__(self): return self.name


class Gig(models.Model):
    class Status(models.TextChoices):
        DRAFT='draft','Draft'; OPEN='open','Open'; IN_PROGRESS='in_progress','In progress'; COMPLETED='completed','Completed'; CANCELLED='cancelled','Cancelled'; HIDDEN='hidden','Hidden'
    class BudgetType(models.TextChoices):
        FIXED='fixed','Fixed price'; HOURLY='hourly','Hourly'
    class ExperienceLevel(models.TextChoices):
        ENTRY='entry','Entry level'; INTERMEDIATE='intermediate','Intermediate'; EXPERT='expert','Expert'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gigs')
    category = models.ForeignKey(GigCategory, on_delete=models.PROTECT, related_name='gigs')
    title = models.CharField(max_length=180)
    description = models.TextField()
    skills = models.ManyToManyField(Skill, related_name='gigs', blank=True)
    budget_type = models.CharField(max_length=20, choices=BudgetType.choices, default=BudgetType.FIXED)
    budget = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    deadline = models.DateField()
    experience_level = models.CharField(max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.ENTRY)
    attachment = models.FileField(upload_to='gig_attachments/', blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['status','created_at']), models.Index(fields=['category','status'])]

    def __str__(self): return self.title
    def get_absolute_url(self): return reverse('marketplace:gig_detail', kwargs={'pk': self.pk})


class Proposal(models.Model):
    class Status(models.TextChoices):
        PENDING='pending','Pending'; SHORTLISTED='shortlisted','Shortlisted'; ACCEPTED='accepted','Accepted'; REJECTED='rejected','Rejected'; WITHDRAWN='withdrawn','Withdrawn'

    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name='proposals')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proposals')
    cover_letter = models.TextField()
    proposed_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    delivery_days = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    milestones = models.TextField(blank=True)
    attachment = models.FileField(upload_to='proposal_attachments/', blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['gig','applicant'], name='unique_proposal_per_gig')]


class SavedGig(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_gigs')
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user','gig'], name='unique_saved_gig')]
