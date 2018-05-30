from django.shortcuts import render, redirect, get_object_or_404
import threading
import os

from .models import Request
from .forms import DocumentForm, RequestForm


def home(request):
    if request.user.is_authenticated:
        documents = request.user.your_documents.all()
        doc_name = [os.path.basename(i.document.name) for i in documents]
        return render(request, 'video_service/home.html', {'doc_name': doc_name})
    else:
        return render(request, 'video_service/home.html')


def process(request, name):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = RequestForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                for doc in request.user.your_documents.all():
                    if os.path.basename(doc.document.name) == name:
                        obj.document = doc
                obj.save()
                thread = threading.Thread(target=obj.proceed_request)
                thread.start()
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
