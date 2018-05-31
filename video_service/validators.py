from django.core.exceptions import ValidationError
import os


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', 'mkv']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Не поддерживаемый тип. Возможные типы: mp4, mkv')


def validate_crf_value(value):
    if value > 52 or value < 0:
        raise ValidationError(u'Неверное значение crf. Диапазон: [0, 51]')

