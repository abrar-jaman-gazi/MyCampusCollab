from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import GigForm, ProposalForm
from .models import Gig, GigCategory, Proposal, SavedGig
from apps.accounts.models import Skill
from apps.communication.models import Notification


def gig_list(request):
    gigs=Gig.objects.filter(status=Gig.Status.OPEN).select_related('owner','owner__profile','category').prefetch_related('skills')
    q=request.GET.get('q','').strip(); category=request.GET.get('category',''); skill=request.GET.get('skill',''); sort=request.GET.get('sort','newest')
    if q: gigs=gigs.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(skills__name__icontains=q)).distinct()
    if category: gigs=gigs.filter(category__slug=category)
    if skill: gigs=gigs.filter(skills__slug=skill)
    if request.GET.get('min_budget'): gigs=gigs.filter(budget__gte=request.GET['min_budget'])
    if sort=='budget_high': gigs=gigs.order_by('-budget')
    elif sort=='deadline': gigs=gigs.order_by('deadline')
    return render(request,'marketplace/gig_list.html',{'gigs':gigs[:80],'categories':GigCategory.objects.filter(is_active=True),'skills':Skill.objects.filter(is_active=True),'q':q})


def gig_detail(request,pk):
    gig=get_object_or_404(Gig.objects.select_related('owner','owner__profile','category').prefetch_related('skills'),pk=pk)
    if gig.status==Gig.Status.HIDDEN and (not request.user.is_authenticated or request.user!=gig.owner):
        messages.error(request,'This gig is not available.');return redirect('marketplace:gig_list')
    Gig.objects.filter(pk=pk).update(views=gig.views+1)
    applied=request.user.is_authenticated and Proposal.objects.filter(gig=gig,applicant=request.user).exists()
    saved=request.user.is_authenticated and SavedGig.objects.filter(gig=gig,user=request.user).exists()
    similar=Gig.objects.filter(status=Gig.Status.OPEN,category=gig.category).exclude(pk=gig.pk).select_related('owner','category')[:3]
    return render(request,'marketplace/gig_detail.html',{'gig':gig,'applied':applied,'saved':saved,'similar':similar})

@login_required
def gig_create(request):
    form=GigForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        gig=form.save(commit=False);gig.owner=request.user;gig.save();form.save_m2m();messages.success(request,'Gig published successfully.');return redirect(gig)
    return render(request,'marketplace/gig_form.html',{'form':form,'title':'Post a new gig'})

@login_required
def gig_edit(request,pk):
    gig=get_object_or_404(Gig,pk=pk,owner=request.user);form=GigForm(request.POST or None,request.FILES or None,instance=gig)
    if request.method=='POST' and form.is_valid(): form.save();messages.success(request,'Gig updated.');return redirect(gig)
    return render(request,'marketplace/gig_form.html',{'form':form,'title':'Edit gig'})

@login_required
def gig_delete(request,pk):
    gig=get_object_or_404(Gig,pk=pk,owner=request.user)
    if request.method=='POST': gig.delete();messages.success(request,'Gig deleted.');return redirect('marketplace:my_gigs')
    return render(request,'shared/confirm_delete.html',{'object':gig,'title':'Delete gig'})

@login_required
def my_gigs(request):
    return render(request,'marketplace/my_gigs.html',{'gigs':request.user.gigs.select_related('category').prefetch_related('skills')})

@login_required
def submit_proposal(request,pk):
    gig=get_object_or_404(Gig,pk=pk,status=Gig.Status.OPEN)
    if gig.owner==request.user: messages.error(request,'You cannot submit a proposal to your own gig.');return redirect(gig)
    if Proposal.objects.filter(gig=gig,applicant=request.user).exists(): messages.info(request,'You already submitted a proposal.');return redirect(gig)
    form=ProposalForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        proposal=form.save(commit=False);proposal.gig=gig;proposal.applicant=request.user;proposal.save()
        Notification.objects.create(recipient=gig.owner,actor=request.user,notification_type='proposal',title='New proposal received',message=f'{request.user.display_name} applied to {gig.title}',url=f'/gigs/{gig.pk}/proposals/')
        messages.success(request,'Proposal submitted.');return redirect('marketplace:my_proposals')
    return render(request,'marketplace/proposal_form.html',{'form':form,'gig':gig})

@login_required
def my_proposals(request):
    proposals=request.user.proposals.select_related('gig','gig__owner','gig__category')
    return render(request,'marketplace/my_proposals.html',{'proposals':proposals})

@login_required
def received_proposals(request,pk):
    gig=get_object_or_404(Gig,pk=pk,owner=request.user)
    proposals=gig.proposals.select_related('applicant','applicant__profile')
    return render(request,'marketplace/received_proposals.html',{'gig':gig,'proposals':proposals})

@login_required
@transaction.atomic
def proposal_status(request,pk,status):
    proposal=get_object_or_404(Proposal.objects.select_related('gig','applicant'),pk=pk,gig__owner=request.user)
    allowed={Proposal.Status.SHORTLISTED,Proposal.Status.ACCEPTED,Proposal.Status.REJECTED}
    if request.method=='POST' and status in allowed:
        proposal.status=status;proposal.save(update_fields=['status','updated_at'])
        if status==Proposal.Status.ACCEPTED:
            proposal.gig.status=Gig.Status.IN_PROGRESS;proposal.gig.save(update_fields=['status'])
            proposal.gig.proposals.exclude(pk=proposal.pk).filter(status__in=[Proposal.Status.PENDING,Proposal.Status.SHORTLISTED]).update(status=Proposal.Status.REJECTED)
        Notification.objects.create(recipient=proposal.applicant,actor=request.user,notification_type='proposal',title=f'Proposal {proposal.get_status_display()}',message=f'Your proposal for {proposal.gig.title} was {proposal.get_status_display().lower()}.',url=f'/gigs/{proposal.gig.pk}/')
        messages.success(request,f'Proposal marked {proposal.get_status_display().lower()}.')
    return redirect('marketplace:received_proposals',pk=proposal.gig.pk)

@login_required
def save_gig(request,pk):
    gig=get_object_or_404(Gig,pk=pk)
    obj,created=SavedGig.objects.get_or_create(user=request.user,gig=gig)
    if not created: obj.delete()
    if request.headers.get('x-requested-with')=='XMLHttpRequest': return JsonResponse({'saved':created})
    return redirect(gig)
