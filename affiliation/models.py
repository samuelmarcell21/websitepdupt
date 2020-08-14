from django.db import connections
from django.db import models

# Create your models here.
class Affiliations(models.Model):
    id_univ = models.CharField(max_length=25,primary_key=True,db_column="id_univ")
    name = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    class Meta:
        db_table = "university"