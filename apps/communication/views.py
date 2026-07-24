from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import MessageForm
from .models import Conversation, Message, Notification
from apps.accounts.models import User

@login_required
def inbox(request,conversation_id=None):
    conversations=request.user.conversations.annotate(last_activity=Max('messages__created_at')).order_by('-last_activity','-updated_at').prefetch_related('participants','messages')
    active=None;other=None;form=MessageForm()
    if conversation_id:
        active=get_object_or_404(conversations,pk=conversation_id)
        other=active.participants.exclude(pk=request.user.pk).first()
        active.messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)
    rows=[]
    for c in conversations:
        rows.append({'conversation':c,'other':c.participants.exclude(pk=request.user.pk).first(),'last':c.messages.last()})
    return render(request,'communication/inbox.html',{'conversation_rows':rows,'active':active,'other':other,'form':form})

@login_required
def start_conversation(request,username):
    other=get_object_or_404(User,username=username,is_active=True)
    if other==request.user: return redirect('communication:inbox')
    matches=request.user.conversations.filter(participants=other)
    conversation=next((c for c in matches if c.participants.count()==2),None)
    if not conversation:
        conversation=Conversation.objects.create();conversation.participants.add(request.user,other)
    return redirect('communication:conversation',conversation_id=conversation.pk)

@login_required
def send_message(request,conversation_id):
    conversation=get_object_or_404(request.user.conversations,pk=conversation_id)
    if request.method!='POST': return JsonResponse({'error':'POST required'},status=405)
    form=MessageForm(request.POST,request.FILES)
    if form.is_valid():
        msg=form.save(commit=False);msg.conversation=conversation;msg.sender=request.user;msg.save();conversation.updated_at=timezone.now();conversation.save(update_fields=['updated_at'])
        recipient=conversation.participants.exclude(pk=request.user.pk).first()
        if recipient: Notification.objects.create(recipient=recipient,actor=request.user,notification_type='message',title='New message',message=f'{request.user.display_name} sent you a message.',url=f'/communication/messages/{conversation.pk}/')
        if request.headers.get('x-requested-with')=='XMLHttpRequest': return JsonResponse({'ok':True,'body':msg.body,'created':msg.created_at.strftime('%I:%M %p')})
        return redirect('communication:conversation',conversation_id=conversation.pk)
    if request.headers.get('x-requested-with')=='XMLHttpRequest': return JsonResponse({'error':form.errors.as_text()},status=400)
    messages.error(request,'Message could not be sent.');return redirect('communication:conversation',conversation_id=conversation.pk)

@login_required
def notifications(request):
    items=request.user.notifications.all()
    kind=request.GET.get('type','')
    if kind: items=items.filter(notification_type=kind)
    return render(request,'communication/notifications.html',{'notifications':items[:100],'types':Notification.Type.choices})

@login_required
def notification_read(request,pk):
    item=get_object_or_404(Notification,pk=pk,recipient=request.user);item.is_read=True;item.save(update_fields=['is_read'])
    return redirect(item.url or 'communication:notifications')

@login_required
def mark_all_read(request):
    if request.method=='POST': request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('communication:notifications')
