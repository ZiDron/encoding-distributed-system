from django.shortcuts import render, redirect, get_object_or_404

from .models import Document, Request
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
                obj.save()
                obj.get_description()
                return redirect('/')
        else:
            form = RequestForm()
        return render(request, 'video_service/request.html', {
            'form': form
        })
    else:
        return redirect('auth_login')

    return render(request, 'video_service/show_request.html')


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


def show_request(request, name):
    if request.user.is_authenticated:
        user_request = get_object_or_404(Request, name=name)
        return render(request, 'video_service/show_request.html', {'request': user_request})
    else:
        return redirect('auth_login')
    return render(request, 'video_service/show_request.html')