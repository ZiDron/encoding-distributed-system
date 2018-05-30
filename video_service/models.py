from django.db import models
from django.contrib.auth.models import User
from subprocess import Popen, PIPE

from .validators import validate_file_extension


def user_directory_path(instance, filename):
    return 'documents/{0}/{1}'.format(instance.user.username, filename)


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='your_documents', default=1)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_request', default=1)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='requets_list')
    name = models.CharField(max_length=255, blank=True)

    description = models.BooleanField(default=False)
    # video_to_images = models.BooleanField(default=False)
    get_music = models.BooleanField(default=False)

    def proceed_request(self):
        if self.description:
            process = Popen("c:/ffmpeg-20180528-ebf85d3-win64-static/bin/ffmpeg.exe -i \""
                            + self.document.document.path + "\"", shell=True, stdout=PIPE)
            data = process.communicate()
            print(data)


# class Answer(models.Model):
#     request = models.OneToOneField(Request, on_delete=models.CASCADE, related_name='answer')

