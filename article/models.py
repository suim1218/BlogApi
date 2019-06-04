from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=10, )
    author = models.CharField(max_length=10)
    content = models.CharField(max_length=500)
    date_publish = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title