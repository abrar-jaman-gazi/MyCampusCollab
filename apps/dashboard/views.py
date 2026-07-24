from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from apps.accounts.decorators import admin_required
from apps.accounts.models import Skill, User
from apps.collaboration.models import CollaborationProject, JoinRequest, ProjectCategory
from apps.communication.models import Message, Notification
from apps.engagement.models import AdminAction, Report, Review
from apps.marketplace.models import Gig, GigCategory, Proposal


def landing(request):
    featured_gigs=Gig.objects.filter(status='open').select_related('owner','category').prefetch_related('skills')[:6]
    featured_projects=CollaborationProject.objects.filter(status__in=['recruiting','active']).select_related('owner','category').prefetch_related('skills','members')[:4]
    stats={'students':User.objects.filter(role='student').count(),'gigs':Gig.objects.filter(status='open').count(),'projects':CollaborationProject.objects.filter(status__in=['recruiting','active']).count(),'collaborations':Proposal.objects.filter(status='accepted').count()+JoinRequest.objects.filter(status='accepted').count()}
    return render(request,'landing.html',{'featured_gigs':featured_gigs,'featured_projects':featured_projects,'stats':stats,'skills':Skill.objects.filter(is_active=True)[:8]})

@login_required
def dashboard_home(request):
    if request.user.role=='admin' or request.user.is_superuser: return redirect('dashboard:admin_home')
    upcoming_gigs=request.user.gigs.filter(deadline__gte=timezone.localdate()).order_by('deadline')[:5]
    upcoming_projects=request.user.owned_projects.filter(end_date__gte=timezone.localdate()).order_by('end_date')[:5]
    recommended_gigs=Gig.objects.filter(status='open').exclude(owner=request.user).select_related('owner','category').prefetch_related('skills')[:4]
    recommended_projects=CollaborationProject.objects.filter(status='recruiting').exclude(owner=request.user).select_related('owner','category').prefetch_related('skills','members')[:3]
    context={'posted_gigs':request.user.gigs.count(),'submitted_proposals':request.user.proposals.count(),'active_projects':request.user.project_memberships.filter(project__status='active').count(),'completed_projects':request.user.project_memberships.filter(project__status='completed').count(),'rating':round(request.user.reviews_received.aggregate(v=Avg('quality'))['v'] or 0,1),'recent_notifications':request.user.notifications.all()[:5],'recent_messages':Message.objects.filter(conversation__participants=request.user).select_related('sender').order_by('-created_at')[:5],'upcoming_gigs':upcoming_gigs,'upcoming_projects':upcoming_projects,'recommended_gigs':recommended_gigs,'recommended_projects':recommended_projects}
    return render(request,'dashboard/student_dashboard.html',context)

@admin_required
def admin_home(request):
    thirty_days=timezone.now()-timedelta(days=30)
    context={'total_users':User.objects.count(),'active_users':User.objects.filter(is_active=True,is_suspended=False).count(),'suspended_users':User.objects.filter(is_suspended=True).count(),'total_gigs':Gig.objects.count(),'active_projects':CollaborationProject.objects.filter(status__in=['recruiting','active']).count(),'proposals':Proposal.objects.count(),'open_reports':Report.objects.filter(status='open').count(),'recent_users':User.objects.order_by('-date_joined')[:6],'recent_reports':Report.objects.select_related('reporter')[:6],'category_data':list(GigCategory.objects.annotate(total=Count('gigs')).values('name','total')[:8])}
    return render(request,'dashboard/admin_dashboard.html',context)

@admin_required
def admin_users(request):
    users=User.objects.select_related('profile').order_by('-date_joined');q=request.GET.get('q','').strip();status=request.GET.get('status','')
    if q: users=users.filter(Q(email__icontains=q)|Q(username__icontains=q)|Q(first_name__icontains=q)|Q(last_name__icontains=q))
    if status=='suspended': users=users.filter(is_suspended=True)
    elif status=='active': users=users.filter(is_suspended=False,is_active=True)
    return render(request,'dashboard/admin_users.html',{'users':users[:100],'q':q})

@admin_required
def toggle_suspend(request,pk):
    user=get_object_or_404(User,pk=pk)
    if request.method=='POST' and user!=request.user:
        user.is_suspended=not user.is_suspended;user.save(update_fields=['is_suspended'])
        AdminAction.objects.create(admin=request.user,action='Suspended user' if user.is_suspended else 'Reactivated user',target_type='user',target_id=user.pk)
        Notification.objects.create(recipient=user,actor=request.user,notification_type='admin',title='Account status updated',message='Your account was suspended.' if user.is_suspended else 'Your account was reactivated.')
        messages.success(request,'User status updated.')
    return redirect('dashboard:admin_users')

@admin_required
def admin_content(request):
    return render(request,'dashboard/admin_content.html',{'gigs':Gig.objects.select_related('owner','category')[:80],'projects':CollaborationProject.objects.select_related('owner','category')[:80]})

@admin_required
def toggle_content(request,kind,pk):
    model=Gig if kind=='gig' else CollaborationProject;obj=get_object_or_404(model,pk=pk)
    if request.method=='POST':
        obj.status='open' if kind=='gig' and obj.status=='hidden' else ('recruiting' if kind=='project' and obj.status=='hidden' else 'hidden');obj.save(update_fields=['status']);AdminAction.objects.create(admin=request.user,action='Toggled content visibility',target_type=kind,target_id=obj.pk)
    return redirect('dashboard:admin_content')

@admin_required
def admin_reports(request):
    reports=Report.objects.select_related('reporter');status=request.GET.get('status','')
    if status: reports=reports.filter(status=status)
    return render(request,'dashboard/admin_reports.html',{'reports':reports,'statuses':Report.Status.choices})

@admin_required
def resolve_report(request,pk,status):
    report=get_object_or_404(Report,pk=pk)
    if request.method=='POST' and status in [Report.Status.RESOLVED,Report.Status.DISMISSED,Report.Status.INVESTIGATING]: report.status=status;report.save(update_fields=['status','updated_at']);AdminAction.objects.create(admin=request.user,action=f'Report {status}',target_type='report',target_id=report.pk);messages.success(request,'Report status updated.')
    return redirect('dashboard:admin_reports')
