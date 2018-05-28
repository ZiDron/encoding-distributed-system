from django.shortcuts import render, redirect

from .models import Document
from .forms import DocumentForm, RequestForm


def home(request):
    documents = Document.objects.all()
    return render(request, 'video_service/home.html', {'documents': documents})


def process(request, name):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = RequestForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                for i in Document.objects.all():
                    if i.document.name == 'documents/' + name:
                        obj.document = i
                print("OLOLOLOLO")
                print(obj)
                obj.save()
                return redirect('/')
        else:
            form = RequestForm()
        return render(request, 'video_service/request.html', {
            'form': form
        })
    else:
        return redirect('auth_login')

    return render(request, 'video_service/processing.html')


def model_form_upload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                return redirect('/')
        else:
            form = DocumentForm()
        return render(request, 'video_service/model_form_upload.html', {
            'form': form
        })
    else:
        return redirect('auth_login')
