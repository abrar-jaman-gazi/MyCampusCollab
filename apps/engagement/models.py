from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Review(models.Model):
    reviewer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reviews_given')
    recipient=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reviews_received')
    gig=models.ForeignKey('marketplace.Gig',on_delete=models.SET_NULL,null=True,blank=True,related_name='reviews')
    project=models.ForeignKey('collaboration.CollaborationProject',on_delete=models.SET_NULL,null=True,blank=True,related_name='reviews')
    communication=models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    quality=models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    teamwork=models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    punctuality=models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-created_at']
        constraints=[
            models.CheckConstraint(condition=models.Q(gig__isnull=False)|models.Q(project__isnull=False),name='review_has_context'),
            models.UniqueConstraint(fields=['reviewer','recipient','gig'],condition=models.Q(gig__isnull=False),name='unique_gig_review'),
            models.UniqueConstraint(fields=['reviewer','recipient','project'],condition=models.Q(project__isnull=False),name='unique_project_review'),
        ]
    @property
    def average(self): return round((self.communication+self.quality+self.teamwork+self.punctuality)/4,1)

class Report(models.Model):
    class Target(models.TextChoices): USER='user','User'; GIG='gig','Gig'; PROJECT='project','Project'; MESSAGE='message','Message'; REVIEW='review','Review'
    class Status(models.TextChoices): OPEN='open','Open'; INVESTIGATING='investigating','Investigating'; RESOLVED='resolved','Resolved'; DISMISSED='dismissed','Dismissed'
    reporter=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reports_made')
    target_type=models.CharField(max_length=20,choices=Target.choices)
    target_id=models.PositiveBigIntegerField()
    reason=models.CharField(max_length=180)
    description=models.TextField()
    evidence=models.FileField(upload_to='report_evidence/',blank=True)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.OPEN)
    admin_notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-created_at']

class AdminAction(models.Model):
    admin=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='admin_actions')
    action=models.CharField(max_length=160)
    target_type=models.CharField(max_length=80)
    target_id=models.PositiveBigIntegerField()
    notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
