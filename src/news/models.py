from django.db import models


class News(models.Model):
    channel = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=2000)
    tag = models.CharField(max_length=250)
    publish_date = models.DateField(auto_now=True)

