from django import forms
from .models import MpTopic, MpEntry, MpUsuarioChurrasco

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

class MpUsuarioChurrascoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define os campos que devem ser ocultos
        # self.fields['resultado'].widget.attrs['style'] = 'display: none'

    class Meta:
        model = MpUsuarioChurrasco
        fields = ['cep', 'cpf', 'qtdPessoas']
        labels = {'cep': 'CEP:', 'cpf': 'CPF:', 'qtdPessoas': 'No.Convidados:'}
        # widgets = {'resultado': forms.Textarea(attrs={'cols': 80, 'readonly': True})}