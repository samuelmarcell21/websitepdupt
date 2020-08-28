from django.db import connections
from django.db import models
from topic.models import Topics
from affiliation.models import Affiliations

# Create your models here.
class Authors(models.Model):
    nidn = models.CharField(max_length=25, primary_key=True)
    # id_univ = models.CharField(max_length=25)
    univ = models.ForeignKey(Affiliations, on_delete=models.CASCADE,db_column="id_univ",to_field='id_univ',related_name="aut")
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
    topik_dominan1 = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="topik_dominan1",to_field='id_topic',related_name="topik_dominan1_aut")
    nilai_dominan1 = models.IntegerField()
    topik_dominan2 = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="topik_dominan2",to_field='id_topic',related_name="topik_dominan2_aut")
    nilai_dominan2 = models.IntegerField()
    topik_dominan3 = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="topik_dominan3",to_field='id_topic',related_name="topik_dominan3_aut")
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
    id_pub = models.CharField(max_length=25,primary_key=True)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE,db_column="nidn",to_field='nidn',related_name="paper")
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
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="id_topic",to_field='id_topic',related_name="id_topic_paper")
    subtopic = models.CharField(max_length=20 , db_column="id_subtopic")
    flag = models.IntegerField()
    class Meta:
        db_table = "dataset_publication"

class Papers_Update(models.Model):
    id_pub = models.CharField(max_length=25,primary_key=True)
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
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="id_topic",to_field='id_topic',related_name="id_topic_paper1")
    subtopic = models.CharField(max_length=20)
    flag = models.IntegerField()
    class Meta:
        db_table = "dataset_publication_update"       
 
class Svg_top(models.Model):
    id = models.CharField(max_length=25, primary_key=True)
    # id_topic = models.CharField(max_length=25)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="id_topic",related_name="svg",to_field='id_topic')
    Year = models.CharField(max_length=25)
    kumAtas = models.CharField(max_length=25)
    kumBawah = models.CharField(max_length=25)
    batasAtas = models.CharField(max_length=25)
    batasBawah = models.CharField(max_length=25)
    class Meta:
        db_table = "svg_top"

class Data_sumcount_author(models.Model):
    id = models.CharField(max_length=25, primary_key=True)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE,db_column="nidn",to_field='nidn',related_name="author_sumcount")
    topic =models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="id_topic",to_field='id_topic',related_name="topik_author_sumcount")
    year = models.CharField(max_length=25)
    pubcount = models.CharField(max_length=25)
    sumcite = models.CharField(max_length=25)
    class Meta:
        db_table = "data_sum_count_author" 