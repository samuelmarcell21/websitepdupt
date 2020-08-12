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
    topik_dominan1 = models.IntegerField()
    nilai_dominan1 = models.IntegerField()
    topik_dominan2 = models.IntegerField()
    nilai_dominan2 = models.IntegerField()
    topik_dominan3 = models.IntegerField()
    nilai_dominan3 = models.IntegerField()
    topik_dominan1_3years = models.IntegerField()
    nilai_dominan1_3years = models.IntegerField()
    topik_dominan2_3years = models.IntegerField()
    nilai_dominan2_3years = models.IntegerField()
    topik_dominan3_3years = models.IntegerField()
    nilai_dominan3_3years = models.IntegerField()
    citations = models.IntegerField()
    h_index = models.IntegerField()
    i10_index = models.IntegerField()
    overall_score = models.FloatField()
    threeyears_score = models.FloatField()
    overall_score_v2 = models.FloatField()
    threeyears_score_v2 = models.FloatField()
    class Meta:
        db_table = "researcher"

class Papers(models.Model):
    id_pub = models.CharField(max_length=25)
    nidn = models.CharField(max_length=25)
    title = models.CharField(max_length=1000)
    cite = models.CharField(max_length=10)
    authors = models.CharField(max_length=2000)
    keywords = models.CharField(max_length=1000)
    abstract = models.CharField(max_length=2000)
    year = models.CharField(max_length=4)
    source_title = models.CharField(max_length=1000)
    volume = models.CharField(max_length=100)
    DOI = models.CharField(max_length=100)
    link = models.CharField(max_length=500)
    class Meta:
        db_table = "dataset_publication"

class Papers_Update(models.Model):
    id_pub = models.CharField(max_length=25)
    nidn = models.CharField(max_length=25)
    title = models.CharField(max_length=1000)
    cite = models.CharField(max_length=10)
    authors = models.CharField(max_length=2000)
    keywords = models.CharField(max_length=1000)
    abstract = models.CharField(max_length=2000)
    year = models.CharField(max_length=4)
    source_title = models.CharField(max_length=1000)
    volume = models.CharField(max_length=100)
    DOI = models.CharField(max_length=100)
    link = models.CharField(max_length=500)
    class Meta:
        db_table = "dataset_publication_update"