from django.db import connections
from django.db import models
from topic.models import Topics

# Create your models here.
class Affiliations(models.Model):
    id_univ = models.CharField(max_length=25,primary_key=True,db_column="id_univ")
    name = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    topik_dominan1 = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="topik_dominan1",to_field='id_topic',related_name="topik_dominan1")
    nilai_dominan1 = models.IntegerField()
    topik_dominan2 = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="topik_dominan2",to_field='id_topic',related_name="topik_dominan2")
    nilai_dominan2 = models.IntegerField()
    topik_dominan3 = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="topik_dominan3",to_field='id_topic',related_name="topik_dominan3")
    nilai_dominan3 = models.IntegerField()
    total_publication = models.IntegerField()
    total_cite = models.IntegerField()
    total_author = models.IntegerField()
    initial_univ = models.CharField(max_length=20)
    class Meta:
        db_table = "university"