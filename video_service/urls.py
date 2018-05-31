from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'video_service'
urlpatterns = [
    path('', views.home, name='home'),
    path('uploads/form/', views.model_form_upload, name='model_form_upload'),
    path('documents/<str:name>/', views.process, name='process'),
    path('request/<str:name>/', views.show_request, name='show_request'),
    path('downloads/<str:name>/', views.send_file, name='send_file'),

    # path('downloads/<str:name>/', views.show_request, name='show_request'),
    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)