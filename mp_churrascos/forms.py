from django import forms
from .models import MpTopic, MpEntry

class MpTopicForm(forms.ModelForm):
    class Meta:
        model = MpTopic
        fields = ['text']
        labels = {'text': ''}

class MpEntryForm(forms.ModelForm):
    class Meta:
        model = MpEntry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
