from bson import ObjectId
from django import template

from ..models import Author

# # Цей блок працював на claud-MongoDB
# from ..utils import get_mongodb

# register = template.Library()


# def get_author(id_):
#     db = get_mongodb()
#     author = db.authors.find_one({"_id": ObjectId(id_)})
#     return author["fullname"]

# # другий параметр -> сигнатура функцiї
# register.filter('author', get_author)


register = template.Library()


@register.filter(name='author')
def get_author(author):
    author_id = author.id if hasattr(author, 'id') else None
    author_instance = Author.objects.filter(id=author_id).first()
    if author_instance:
        return author_instance.fullname
    return ''