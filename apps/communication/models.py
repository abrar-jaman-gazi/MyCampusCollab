from django.conf import settings
from django.db import models

class Conversation(models.Model):
    participants=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='conversations')
    gig=models.ForeignKey('marketplace.Gig',on_delete=models.SET_NULL,null=True,blank=True,related_name='conversations')
    project=models.ForeignKey('collaboration.CollaborationProject',on_delete=models.SET_NULL,null=True,blank=True,related_name='conversations')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-updated_at']

class Message(models.Model):
    conversation=models.ForeignKey(Conversation,on_delete=models.CASCADE,related_name='messages')
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='sent_messages')
    body=models.TextField(blank=True)
    attachment=models.FileField(upload_to='message_attachments/',blank=True)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['created_at']

class Notification(models.Model):
    class Type(models.TextChoices):
        PROPOSAL='proposal','Proposal'; PROJECT='project','Project'; MESSAGE='message','Message'; REVIEW='review','Review'; ADMIN='admin','Admin'; SYSTEM='system','System'
    recipient=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notifications')
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='notifications_created')
    notification_type=models.CharField(max_length=20,choices=Type.choices,default=Type.SYSTEM)
    title=models.CharField(max_length=180)
    message=models.CharField(max_length=300)
    url=models.CharField(max_length=300,blank=True)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']; indexes=[models.Index(fields=['recipient','is_read'])]
