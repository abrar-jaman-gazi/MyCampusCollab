from django import forms
from .models import Message
class MessageForm(forms.ModelForm):
    class Meta:
        model=Message; fields=['body','attachment']; widgets={'body':forms.Textarea(attrs={'rows':2,'placeholder':'Write a message…','class':'message-input'})}
    def clean(self):
        data=super().clean()
        if not data.get('body') and not data.get('attachment'): raise forms.ValidationError('Write a message or attach a file.')
        return data
