from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from wsgiref.util import FileWrapper
import threading
import os

from .models import Request
from django.contrib.auth.models import User
from .forms import DocumentForm, RequestForm


def home(request):
    if request.user.is_authenticated:
        documents = request.user.your_documents.all()
        doc_name = [os.path.basename(i.document.name) for i in documents]
        titles = [i.description for i in documents]
        requests = request.user.user_request.all()
        request_name = [os.path.basename(i.out_document.name) for i in requests]
        print(request_name)
        return render(request, 'video_service/home.html', {'doc_name': doc_name,
                                                           'docs': zip(doc_name, titles),
                                                           'req_name': request_name},
                      )
    else:
        return render(request, 'video_service/home.html')


def process(request, name):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = RequestForm(request.POST, user=request.user)
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


def model_form_upload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES, user=request.user)
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


def send_file(request, name):
    if request.user.is_authenticated:
        print(os.path.split(os.path.abspath(os.path.dirname(__file__))))
        if request.method == 'GET':
            filename = "{0}\\documents\\{1}\\{2}".format(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0],
                                                         request.user.username,
                                                         name)
            file = FileWrapper(open(filename, 'rb'))
            response = HttpResponse(file, content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
            return response
    raise Http404()


def show_profile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User)
        return render(request, 'video_service/profile.html', {'user': user})
    else:
        return redirect('auth_login')

