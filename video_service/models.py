from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='your_documents', default=1)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_request', default=1)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='requets_list')
    description = models.BooleanField()
    name = models.CharField(max_length=255, blank=True)
