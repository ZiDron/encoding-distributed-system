from django import forms
from .models import Document, Request


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document')


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('title', 'description', 'format', 'preset')
        labels = {
            'title':  ('Заголовок'),
            'description': ('Описание'),
            'format': ('Формат'),
            'preset': ('preset')
        }
