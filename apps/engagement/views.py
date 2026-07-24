from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ReportForm, ReviewForm
from .models import Report, Review
from apps.accounts.models import User
from apps.communication.models import Notification

@login_required
def review_create(request,username):
    recipient=get_object_or_404(User,username=username)
    if recipient==request.user: messages.error(request,'You cannot review yourself.');return redirect('accounts:profile',username=username)
    form=ReviewForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        review=form.save(commit=False);review.reviewer=request.user;review.recipient=recipient
        gig_id=request.GET.get('gig');project_id=request.GET.get('project')
        if gig_id: review.gig_id=gig_id
        elif project_id: review.project_id=project_id
        else: form.add_error(None,'A completed gig or project is required.');return render(request,'shared/form_page.html',{'form':form,'title':f'Review {recipient.display_name}','eyebrow':'Trust & reputation','submit_label':'Publish review'})
        review.save();Notification.objects.create(recipient=recipient,actor=request.user,notification_type='review',title='New review received',message=f'{request.user.display_name} left you a review.',url=f'/accounts/u/{recipient.username}/')
        messages.success(request,'Review published.');return redirect('accounts:profile',username=recipient.username)
    return render(request,'shared/form_page.html',{'form':form,'title':f'Review {recipient.display_name}','eyebrow':'Trust & reputation','submit_label':'Publish review'})

@login_required
def report_create(request):
    form=ReportForm(request.POST or None,request.FILES or None,initial={'target_type':request.GET.get('type'),'target_id':request.GET.get('id')})
    if request.method=='POST' and form.is_valid(): report=form.save(commit=False);report.reporter=request.user;report.save();messages.success(request,'Report submitted for administrator review.');return redirect('dashboard:home')
    return render(request,'shared/form_page.html',{'form':form,'title':'Report a concern','eyebrow':'Community safety','submit_label':'Submit report'})
