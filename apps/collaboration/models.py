from django.conf import settings
from django.db import models
from django.urls import reverse
from apps.accounts.models import Skill

class ProjectCategory(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=110,unique=True)
    is_active=models.BooleanField(default=True)
    class Meta: ordering=['name']; verbose_name_plural='Project categories'
    def __str__(self): return self.name

class CollaborationProject(models.Model):
    class Type(models.TextChoices):
        PERSONAL='personal','Personal'; ACADEMIC='academic','Academic'; RESEARCH='research','Research'; STARTUP='startup','Startup'; HACKATHON='hackathon','Hackathon'
    class Status(models.TextChoices):
        RECRUITING='recruiting','Recruiting'; ACTIVE='active','Active'; COMPLETED='completed','Completed'; PAUSED='paused','Paused'; CANCELLED='cancelled','Cancelled'; HIDDEN='hidden','Hidden'
    class WorkMode(models.TextChoices):
        ONLINE='online','Online'; OFFLINE='offline','Offline'; HYBRID='hybrid','Hybrid'

    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='owned_projects')
    category=models.ForeignKey(ProjectCategory,on_delete=models.PROTECT,related_name='projects')
    title=models.CharField(max_length=180)
    project_type=models.CharField(max_length=20,choices=Type.choices)
    description=models.TextField()
    objectives=models.TextField(blank=True)
    skills=models.ManyToManyField(Skill,blank=True,related_name='projects')
    roles_needed=models.CharField(max_length=300,help_text='Comma-separated roles')
    team_size=models.PositiveSmallIntegerField(default=3)
    start_date=models.DateField()
    end_date=models.DateField(null=True,blank=True)
    work_mode=models.CharField(max_length=20,choices=WorkMode.choices,default=WorkMode.ONLINE)
    preference=models.CharField(max_length=200,blank=True)
    attachment=models.FileField(upload_to='project_attachments/',blank=True)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.RECRUITING)
    progress=models.PositiveSmallIntegerField(default=0)
    is_featured=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-created_at']
        indexes=[models.Index(fields=['status','created_at']),models.Index(fields=['project_type','status'])]
    def __str__(self): return self.title
    def get_absolute_url(self): return reverse('collaboration:project_detail',kwargs={'pk':self.pk})
    @property
    def available_positions(self): return max(self.team_size-self.members.filter(status='active').count(),0)

class TeamMember(models.Model):
    class Status(models.TextChoices): ACTIVE='active','Active'; INACTIVE='inactive','Inactive'
    project=models.ForeignKey(CollaborationProject,on_delete=models.CASCADE,related_name='members')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='project_memberships')
    role=models.CharField(max_length=120)
    task_status=models.CharField(max_length=160,blank=True)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)
    joined_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['project','user'],name='unique_project_member')]

class JoinRequest(models.Model):
    class Status(models.TextChoices): PENDING='pending','Pending'; ACCEPTED='accepted','Accepted'; REJECTED='rejected','Rejected'
    project=models.ForeignKey(CollaborationProject,on_delete=models.CASCADE,related_name='join_requests')
    applicant=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='join_requests')
    role=models.CharField(max_length=120)
    message=models.TextField()
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-created_at']
        constraints=[models.UniqueConstraint(fields=['project','applicant'],name='unique_join_request')]

class ProjectUpdate(models.Model):
    project=models.ForeignKey(CollaborationProject,on_delete=models.CASCADE,related_name='updates')
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=180)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
