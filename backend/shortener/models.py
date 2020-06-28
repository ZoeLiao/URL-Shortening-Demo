from django.db import models

from backend.constants import SHORT_PATH_LEN


class URL(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    origin_url = models.URLField(max_length=500, unique=True)
    short_path = models.CharField(max_length=SHORT_PATH_LEN, unique=True)
