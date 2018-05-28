from django import forms
from .models import Document, Request


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document')


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('name', 'description',)
        labels = {
            'name':  ('Название'),
            'description': ('Описание'),
        }