from django.db import models
from django.contrib.auth.models import User


# class Image(models.Model):
    # user = models.ForeignKey(User, related_name='images_created')
    # title = models.CharField(max_length=200)
    # slug = models.SlugField(max_length=200, blank=True)
    # url = models.URLField()
    # image = models.ImageField(upload_to='images/%Y/%m/%d')
    # description = models.TextField(blank=True)
    # created = models.DateField(auto_now_add=True, db_index=True)
    # def __str__(self):
    #     return self.title


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='your_documents', default=1)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)



