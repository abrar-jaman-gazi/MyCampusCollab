from django import forms
from .models import Report, Review
class StyledModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values(): field.widget.attrs.setdefault('class','form-control')
class ReviewForm(StyledModelForm):
    class Meta:
        model=Review; fields=['communication','quality','teamwork','punctuality','comment']; widgets={'comment':forms.Textarea(attrs={'rows':5})}
class ReportForm(StyledModelForm):
    class Meta:
        model=Report; fields=['target_type','target_id','reason','description','evidence']; widgets={'description':forms.Textarea(attrs={'rows':5})}
