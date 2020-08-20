from django.db import connections
from django.db import models

# Create your models here.
class Topics(models.Model):
    id_topic = models.CharField(max_length=20, primary_key=True)
    topic_name = models.CharField(max_length=200)
    total_author = models.IntegerField()
    total_cite = models.IntegerField()
    total_publication = models.IntegerField()
    class Meta:
        db_table = "topic"

class Subtopics(models.Model):
    id_SubTopic = models.CharField(max_length=25, primary_key=True)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="id_topic",to_field='id_topic',related_name="topik_subtopik")
    no_subTopic = models.CharField(max_length=20)
    subtopic_name = models.CharField(max_length=255)

    class Meta:
        db_table = "subtopic"