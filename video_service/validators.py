from django.core.exceptions import ValidationError
import os


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', 'mkv']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Не поддерживаемый тип. Возможные типы: mp4, mkv')