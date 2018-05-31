from django import forms
from .models import Document, Request
import os


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document')
        labels = {
            'description': 'Описание',
            'document': 'Файл'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DocumentForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        super(DocumentForm, self).clean(*args, **kwargs)
        print("Name ", self.user)
        doc_name = [os.path.basename(i.document.name) for i in self.user.your_documents.all()]
        print("Doc name ", doc_name)
        doc = self.cleaned_data.get("document").name
        print("own doc", doc)

        if doc in doc_name:
            raise forms.ValidationError(u'Вы уже загружали этот файл')
        else:
            return self.cleaned_data


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('title', 'description', 'format', 'crf', 'preset')
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'format': 'Формат',
            'crf': 'crf',
            'preset': 'preset'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RequestForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        super(RequestForm, self).clean(*args, **kwargs)
        print("Name ", self.user)
        request_title= [i.title for i in self.user.user_request.all()]
        print("Req title ", request_title)
        req = self.cleaned_data.get("title")
        print("own req", req)

        if req in request_title:
            raise forms.ValidationError(u'Вы уже загружали этот файл')
        else:
            return self.cleaned_data
