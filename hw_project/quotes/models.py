from django.db import models
from django.contrib.auth.models import User


# # Блок видалення автора, якщо цитат з ним бiльше не iснує
# # логiка реалiзована через функцiю [delete_author] з декоратором @receiver
# # але наразi для цого проекту видалення цього зв'язку та запису автора
# # перенесено у функцiю [delete_quote] файлу views.py
# from django.db.models.signals import post_delete
# from django.dispatch import receiver


# @receiver(post_delete, sender=Quote)
# def delete_author(sender, instance, **kwargs):
#     if instance.author.quotes.count() == 0:
#         instance.author.delete()


class Author(models.Model):
    fullname = models.CharField(max_length=64, null=False, unique=True)
    born_date = models.CharField(max_length=64)
    born_location = models.CharField(max_length=256)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=16, null=False, unique=True)
    
    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"


# class Quote(models.Model):
#     quote = models.TextField()
#     tags = models.ManyToManyField(Tag)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=False)
    created_at = models.DateTimeField(auto_now_add=True)