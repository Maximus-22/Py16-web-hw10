from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


from .forms import QuoteForm, AuthorForm
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


@login_required
def add_quote(request):
    if request.method == 'POST':
        quote_form = QuoteForm(request.POST)
        author_form = AuthorForm(request.POST)
        if quote_form.is_valid() and author_form.is_valid():
            # Обробка автора
            author = author_form.save()

            # Обробка цитати
            quote = quote_form.save(commit=False)
            quote.user = request.user
            quote.author = author
            quote.save()

            # Обробка тегів для ManyToManyField
            tags = quote_form.cleaned_data['tags']

            # Проблема у тому, що у поле <tags> об'єкту [Quotes] потрiбно вставити перелiченi об'єкти [Tag]
            # Наступна конструкцiя намагається знайти об'єкт [Tag] у iснуючий базі даних за вказаним ім'ям.
            # Якщо об'єкт з такою назвою вже існує, він повертається. В іншому випадку, створюється новий
            # об'єкт Tag із зазначеним ім'ям.
            # Що стосується [0], це просто вилучення першого елемента з кортежу, який повертає [get_or_create].
            # Цей кортеж містить два значення: об'єкт [Tag] та прапор, який вказує, чи був об'єкт створений
            # (True, якщо створено, і False, якщо вже існує). Оскільки нам потрібен лише сам об'єкт [Tag],
            # ми використовуємо [0], щоб отримати його.
            tag_objects = [Tag.objects.get_or_create(name=tag.strip())[0] for tag in tags]

            # Використання методу [set] для встановлення зв'язків між цитатою та об'єктами тегів, якi представленi
            # у [tag_objects]
            quote.tags.set(tag_objects)
            
            # Перенаправлення на сторінку зі списком цитат
            return redirect(to='quotes:root')  
    else:
        quote_form = QuoteForm()
        author_form = AuthorForm()
    
    return render(request, 'quotes/add_quote.html', {'quote_form': quote_form, 'author_form': author_form})