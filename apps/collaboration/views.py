from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import JoinRequestForm, ProjectForm, ProjectUpdateForm
from .models import CollaborationProject, JoinRequest, ProjectCategory, ProjectUpdate, TeamMember
from apps.accounts.models import Skill
from apps.communication.models import Notification


def project_list(request):
    projects=CollaborationProject.objects.filter(status__in=[CollaborationProject.Status.RECRUITING,CollaborationProject.Status.ACTIVE]).select_related('owner','owner__profile','category').prefetch_related('skills','members')
    q=request.GET.get('q','').strip();ptype=request.GET.get('type','');category=request.GET.get('category','');mode=request.GET.get('mode','')
    if q: projects=projects.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(skills__name__icontains=q)|Q(roles_needed__icontains=q)).distinct()
    if ptype: projects=projects.filter(project_type=ptype)
    if category: projects=projects.filter(category__slug=category)
    if mode: projects=projects.filter(work_mode=mode)
    return render(request,'collaboration/project_list.html',{'projects':projects[:80],'categories':ProjectCategory.objects.filter(is_active=True),'types':CollaborationProject.Type.choices,'q':q})


def project_detail(request,pk):
    project=get_object_or_404(CollaborationProject.objects.select_related('owner','owner__profile','category').prefetch_related('skills','members__user__profile','updates__author'),pk=pk)
    requested=request.user.is_authenticated and JoinRequest.objects.filter(project=project,applicant=request.user).exists()
    is_member=request.user.is_authenticated and TeamMember.objects.filter(project=project,user=request.user,status='active').exists()
    return render(request,'collaboration/project_detail.html',{'project':project,'requested':requested,'is_member':is_member})

@login_required
def project_create(request):
    form=ProjectForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        project=form.save(commit=False);project.owner=request.user;project.save();form.save_m2m();TeamMember.objects.create(project=project,user=request.user,role='Project owner')
        messages.success(request,'Project published.');return redirect(project)
    return render(request,'collaboration/project_form.html',{'form':form,'title':'Create collaboration project'})

@login_required
def project_edit(request,pk):
    project=get_object_or_404(CollaborationProject,pk=pk,owner=request.user);form=ProjectForm(request.POST or None,request.FILES or None,instance=project)
    if request.method=='POST' and form.is_valid(): form.save();messages.success(request,'Project updated.');return redirect(project)
    return render(request,'collaboration/project_form.html',{'form':form,'title':'Edit project'})

@login_required
def project_delete(request,pk):
    project=get_object_or_404(CollaborationProject,pk=pk,owner=request.user)
    if request.method=='POST': project.delete();messages.success(request,'Project deleted.');return redirect('collaboration:my_projects')
    return render(request,'shared/confirm_delete.html',{'object':project,'title':'Delete project'})

@login_required
def my_projects(request):
    owned=request.user.owned_projects.select_related('category').prefetch_related('members')
    joined=CollaborationProject.objects.filter(members__user=request.user,members__status='active').exclude(owner=request.user).distinct()
    return render(request,'collaboration/my_projects.html',{'owned':owned,'joined':joined})

@login_required
def join_project(request,pk):
    project=get_object_or_404(CollaborationProject,pk=pk,status=CollaborationProject.Status.RECRUITING)
    if project.owner==request.user: messages.info(request,'You own this project.');return redirect(project)
    if TeamMember.objects.filter(project=project,user=request.user).exists(): messages.info(request,'You are already a member.');return redirect(project)
    existing=JoinRequest.objects.filter(project=project,applicant=request.user).first()
    if existing: messages.info(request,'You already requested to join.');return redirect(project)
    form=JoinRequestForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        req=form.save(commit=False);req.project=project;req.applicant=request.user;req.save()
        Notification.objects.create(recipient=project.owner,actor=request.user,notification_type='project',title='New join request',message=f'{request.user.display_name} wants to join {project.title}',url=f'/projects/{project.pk}/team/')
        messages.success(request,'Join request sent.');return redirect(project)
    return render(request,'shared/form_page.html',{'form':form,'title':f'Join {project.title}','eyebrow':'Collaboration','submit_label':'Send request'})

@login_required
def team_manage(request,pk):
    project=get_object_or_404(CollaborationProject,pk=pk,owner=request.user)
    return render(request,'collaboration/team_manage.html',{'project':project,'members':project.members.select_related('user','user__profile'),'requests':project.join_requests.select_related('applicant','applicant__profile')})

@login_required
@transaction.atomic
def join_request_status(request,pk,status):
    req=get_object_or_404(JoinRequest.objects.select_related('project','applicant'),pk=pk,project__owner=request.user)
    if request.method=='POST' and status in [JoinRequest.Status.ACCEPTED,JoinRequest.Status.REJECTED]:
        if status==JoinRequest.Status.ACCEPTED:
            if req.project.available_positions<=0: messages.error(request,'The team is already full.');return redirect('collaboration:team_manage',pk=req.project.pk)
            TeamMember.objects.get_or_create(project=req.project,user=req.applicant,defaults={'role':req.role})
        req.status=status;req.save(update_fields=['status'])
        Notification.objects.create(recipient=req.applicant,actor=request.user,notification_type='project',title=f'Join request {req.get_status_display()}',message=f'Your request for {req.project.title} was {req.get_status_display().lower()}.',url=f'/projects/{req.project.pk}/')
        messages.success(request,f'Request {req.get_status_display().lower()}.')
    return redirect('collaboration:team_manage',pk=req.project.pk)

@login_required
def remove_member(request,pk,member_id):
    project=get_object_or_404(CollaborationProject,pk=pk,owner=request.user);member=get_object_or_404(TeamMember,pk=member_id,project=project)
    if request.method=='POST' and member.user!=project.owner: member.delete();messages.success(request,'Team member removed.')
    return redirect('collaboration:team_manage',pk=project.pk)

@login_required
def add_update(request,pk):
    project=get_object_or_404(CollaborationProject,pk=pk)
    if project.owner!=request.user and not TeamMember.objects.filter(project=project,user=request.user,status='active').exists(): messages.error(request,'Only team members can post updates.');return redirect(project)
    form=ProjectUpdateForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): update=form.save(commit=False);update.project=project;update.author=request.user;update.save();messages.success(request,'Project update posted.');return redirect(project)
    return render(request,'shared/form_page.html',{'form':form,'title':'Post project update','eyebrow':'Team update','submit_label':'Post update'})
