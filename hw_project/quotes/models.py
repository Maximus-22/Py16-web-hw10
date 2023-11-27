from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=64)
    born_date = models.CharField(max_length=64)
    born_location = models.CharField(max_length=256)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=32, null=False, unique=True)
    
    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"

class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)