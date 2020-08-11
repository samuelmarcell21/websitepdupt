from django.db import connections
from django.db import models

# Create your models here.
class Topics(models.Model):
    id_topic = models.CharField(max_length=20)
    topic_name = models.CharField(max_length=200)
    total_author = models.IntegerField()
    total_cite = models.IntegerField()
    total_publication = models.IntegerField()
    class Meta:
        db_table = "topic"