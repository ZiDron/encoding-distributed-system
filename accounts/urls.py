from django.urls import path
from . import views as s


urlpatterns = [
    path('signup', s.signup, name='index'),
    path('login', s.ELoginView.as_view(), name='login'),
]