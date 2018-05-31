from django.db import models
from django.contrib.auth.models import User
from subprocess import Popen, PIPE
import os
import time
from django.core.mail import send_mail

from .validators import validate_file_extension, validate_crf_value


def user_directory_path(instance, filename):
    return 'documents/{0}/{1}'.format(instance.user.username, filename)


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='your_documents', default=1)
    description = models.CharField(max_length=255, blank=False)
    document = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document.name


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_request', default=1)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='requets_list')
    title = models.CharField(max_length=255, blank=False, default='')
    description = models.CharField(max_length=255, blank=False, default='')
    # parameters
    PRESET = (
        ('ultrafast', 'ultrafast'),
        ('superfast', 'superfast'),
        ('veryfast', 'veryfast'),
        ('faster', 'faster'),
        ('fast', 'fast'),
        ('medium', 'medium'),
        ('slow', 'slow'),
        ('slower', 'slower'),
        ('veryslow', 'veryslow')
    )
    FORMAT = (
        ('mp4', 'mp4'),
        ('mkv', 'mkv')
    )

    preset = models.CharField(max_length=32, choices=PRESET, default='ultrafast')
    format = models.CharField(max_length=32, choices=FORMAT, default='mp4')
    crf = models.IntegerField(default=23, validators=[validate_crf_value])
    encoding_time = models.BigIntegerField(default=0)

    is_finish = models.BooleanField(default=False)
    out_document = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension], default='')

    def proceed_request(self):
        if self.description:
            start_time = time.time()
            process = Popen("c:/ffmpeg-20180528-ebf85d3-win64-static/bin/ffmpeg.exe -y -i \"{0}\" -f {1}"
                            " -vcodec libx264 -crf {5} -preset {2} \"{3}_{4}.{1}\""
                            .format(self.document.document.path,
                                    self.format,
                                    self.preset,
                                    os.path.splitext(self.document.document.path)[0],
                                    self.title,
                                    str(self.crf)
                                    ),
                            shell=True, stdout=PIPE)
            data = process.communicate()
            self.is_finish = True
            elapsed_time = int((time.time() - start_time) * 1000)
            self.encoding_time = elapsed_time
            self.out_document.name = os.path.splitext(self.document.document.name)[0]\
                                + os.path.splitext(self.document.document.name)[1][:-4]\
                                + "_" + self.title + "." + self.format
            print(self.out_document.name)
            print(self.document.document.name)
            self.save()
            print(self.user.email)
            send_mail('Обработка видео',
                      'Ваш запрос <{0}> на обработку видео завершился.'.format(self.title),
                      'iknow23103gmail.com',
                      [self.user.email],
                      fail_silently=False)

