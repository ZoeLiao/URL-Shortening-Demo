from django.db import models


class URL(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    origin_url = models.URLField(max_length=500, unique=True)
    short_path = models.CharField(max_length=5, unique=True)
