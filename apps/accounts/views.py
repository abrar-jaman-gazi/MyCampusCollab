from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import LoginForm, PortfolioForm, ProfileForm, RegisterForm
from .models import PortfolioItem, Skill, StudentProfile, User


def register_view(request):
    if request.user.is_authenticated: return redirect('dashboard:home')
    form=RegisterForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.save(); login(request,user); messages.success(request,'Welcome to CampusCollab! Complete your profile to get discovered.')
        return redirect('accounts:onboarding')
    return render(request,'accounts/register.html',{'form':form})


def login_view(request):
    if request.user.is_authenticated: return redirect('dashboard:home')
    form=LoginForm(request,data=request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.get_user()
        if user.is_suspended:
            messages.error(request,'This account is suspended.')
        else:
            login(request,user)
            if not form.cleaned_data.get('remember_me'): request.session.set_expiry(0)
            return redirect(request.GET.get('next') or 'dashboard:home')
    return render(request,'accounts/login.html',{'form':form})

@login_required
def logout_view(request):
    if request.method=='POST': logout(request)
    return redirect('home')

@login_required
def onboarding(request):
    profile=request.user.profile
    form=ProfileForm(request.POST or None,request.FILES or None,instance=profile)
    if request.method=='POST' and form.is_valid():
        form.save(); request.user.profile_completed=True; request.user.save(update_fields=['profile_completed'])
        messages.success(request,'Your profile is ready.')
        return redirect('accounts:profile',username=request.user.username)
    return render(request,'accounts/onboarding.html',{'form':form,'progress':profile.completion_percent})

@login_required
def profile_edit(request):
    form=ProfileForm(request.POST or None,request.FILES or None,instance=request.user.profile)
    if request.method=='POST' and form.is_valid():
        form.save(); request.user.profile_completed=True; request.user.save(update_fields=['profile_completed'])
        messages.success(request,'Profile updated successfully.')
        return redirect('accounts:profile',username=request.user.username)
    return render(request,'accounts/profile_form.html',{'form':form})


def profile_detail(request,username):
    student=get_object_or_404(User.objects.select_related('profile'),username=username,role=User.Role.STUDENT)
    reviews=student.reviews_received.select_related('reviewer')[:6]
    rating=student.reviews_received.aggregate(v=Avg('quality'))['v'] or 0
    return render(request,'accounts/profile_detail.html',{'student':student,'reviews':reviews,'rating':round(rating,1)})


def student_directory(request):
    students=User.objects.filter(role=User.Role.STUDENT,is_active=True,is_suspended=False).select_related('profile').prefetch_related('profile__skills')
    q=request.GET.get('q','').strip(); skill=request.GET.get('skill',''); availability=request.GET.get('availability',''); university=request.GET.get('university','').strip()
    if q: students=students.filter(Q(first_name__icontains=q)|Q(last_name__icontains=q)|Q(username__icontains=q)|Q(profile__headline__icontains=q)|Q(profile__skills__name__icontains=q)).distinct()
    if skill: students=students.filter(profile__skills__slug=skill)
    if availability: students=students.filter(profile__availability=availability)
    if university: students=students.filter(profile__university__icontains=university)
    return render(request,'accounts/student_directory.html',{'students':students[:60],'skills':Skill.objects.filter(is_active=True),'q':q})

@login_required
def portfolio_create(request):
    form=PortfolioForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        item=form.save(commit=False);item.owner=request.user;item.save();messages.success(request,'Portfolio project added.')
        return redirect('accounts:profile',username=request.user.username)
    return render(request,'shared/form_page.html',{'form':form,'title':'Add portfolio project','eyebrow':'Portfolio','submit_label':'Add project'})

@login_required
def portfolio_delete(request,pk):
    item=get_object_or_404(PortfolioItem,pk=pk,owner=request.user)
    if request.method=='POST': item.delete();messages.success(request,'Portfolio item removed.');return redirect('accounts:profile',username=request.user.username)
    return render(request,'shared/confirm_delete.html',{'object':item,'title':'Delete portfolio project'})
