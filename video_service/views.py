from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from .models import Document
from .forms import DocumentForm


# def home(request):
#     # context = {
#     #     'product_list': models.Product.objects.filter(is_active=True)[:settings.SHOP_LAST_INCOMING],
#     #     }
#     return render(request, 'video_service/home.html')


def home(request):
    documents = Document.objects.all()
    return render(request, 'video_service/home.html', {'documents': documents})


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
