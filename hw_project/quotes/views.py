from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Author, Quote, Tag
# # Цей блок працював на claud-MongoDB
# from .utils import get_mongodb

# def main(request, page = 1):
#     db = get_mongodb()
#     quotes = db.quotes.find()

#     # робота з пагiнатором
#     elem_per_page = 10
#     paginator = Paginator(list(quotes), elem_per_page)
#     quotes_on_page = paginator.page(page)
#     # return render(request, "quotes/index.html", context={})
#     return render(request, "quotes/index.html", context={"quotes": quotes_on_page})

def main(request, page = 1):
    quotes = Quote.objects.all()

    # робота з пагiнатором
    elem_per_page = 10
    paginator = Paginator(list(quotes), elem_per_page)
    quotes_on_page = paginator.page(page)
    # return render(request, "quotes/index.html", context={})
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, "quotes/author_detail.html", context={"author": author})