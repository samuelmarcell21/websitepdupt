from django.db import connections
from django.db import models

# Create your models here.
class Authors(models.Model):
    nidn = models.CharField(max_length=25)
    id_univ = models.CharField(max_length=25)
    name = models.CharField(max_length=255)
    scholar_id = models.CharField(max_length=255)
    sinta_id = models.CharField(max_length=255)
    scopus_id = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    position = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    rank = models.IntegerField()
    flag = models.IntegerField()
    tag = models.CharField(max_length=300)
    topik_dominan = models.CharField(max_length=25)
    nilai_dominan = models.IntegerField()
    citations = models.IntegerField()
    h_index = models.IntegerField()
    i10_index = models.IntegerField()
    overall_score = models.FloatField()
    threeyears_score = models.FloatField()
    overall_score_v2 = models.FloatField()
    threeyears_score_v2 = models.FloatField()
    class Meta:
        db_table = "researcher"