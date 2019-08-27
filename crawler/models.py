from django.db import models

# Create your models here.

# Create your models here.
class pttdata(models.Model):
    date = models.DateTimeField()
    author = models.TextField()
    title = models.TextField()
    href = models.TextField()
    content=models.TextField(default="")
    pushcount = models.IntegerField()
    # last_modify_date = models.DateTimeField()
    # created = models.DateTimeField()

    class Meta:
        db_table = "crawler"