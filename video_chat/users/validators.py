import os
from django.core.exceptions import ValidationError

def ValidateImageExtesion(value):

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.bmp','.jpg','.jgeg','.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Tipo de archivo invalido.')
