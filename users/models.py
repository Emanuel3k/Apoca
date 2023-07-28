from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import AbstractUser
from django.db import models

from PIL import Image
from io import BytesIO
import sys

class User(AbstractUser):
    foto = models.ImageField(blank=True, default=None, upload_to='fotos/%Y/')
    is_assistente_social = models.BooleanField('Assistente social', default=False)
    is_medico = models.BooleanField('Médico', default=False)
    is_nutricionista = models.BooleanField('Nutricionista', default=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.foto:
            im = Image.open(self.foto)
            output = BytesIO()
            im.thumbnail((512, 512), Image.ANTIALIAS)

            im.save(output, format='JPEG', quality=80)
            output.seek(0)

            self.foto = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" %self.foto.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super(User, self).save()
