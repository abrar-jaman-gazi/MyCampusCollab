from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import PortfolioItem, StudentProfile, User


class StyledFormMixin:
    def apply_styles(self):
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            field.widget.attrs.setdefault('placeholder', field.label)


class RegisterForm(StyledFormMixin, UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()


class LoginForm(StyledFormMixin, AuthenticationForm):
    username = forms.EmailField(label='Email address')
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()


class ProfileForm(StyledFormMixin, forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = StudentProfile
        fields = ['avatar','cover','headline','bio','university','department','location','availability','skills','github_url','linkedin_url','website_url','phone']
        widgets = {'bio': forms.Textarea(attrs={'rows': 5}), 'skills': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        self.apply_styles()
        self.fields['skills'].widget.attrs['class'] = 'skill-checkboxes'

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        if commit:
            profile.user.save(update_fields=['first_name','last_name'])
            profile.save()
            self.save_m2m()
        return profile


class PortfolioForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = ['title','description','technologies','image','github_url','live_url','completed_on']
        widgets = {'description': forms.Textarea(attrs={'rows': 5}), 'completed_on': forms.DateInput(attrs={'type':'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()
