from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View


from .forms import QuoteForm, AuthorForm, AuthorEditForm, DeleteQuoteForm
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
        # if quote_form.is_valid() and author_form.is_valid():
        if quote_form.is_valid():
            # Обробка автора
            # author_name = author_form.cleaned_data['fullname']
            author_name = request.POST.get('fullname')
            print(f"Author Fullname: {author_name}")
            print(f"Quote Form Data: {quote_form.cleaned_data}")
            try:
                # Якщо автор вже існує, тягнемо його дані, щоб прокинути id його створювача
                author = Author.objects.get(fullname=author_name)
                # author.save()
            except Author.DoesNotExist:
                # Якщо автора не існує, створюємо нового
                author = author_form.save(commit=False)
                author.user = request.user
                author.save()
            print(f"Author ID: {author.id}")
            print(f"Author User ID: {author.user_id}")
            print(f"Request User ID: {request.user.id}")

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


@login_required
def edit_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    
    # Перевіряємо, що поточний користувач створював автора
    if request.user.id != author.user.id:
        # Якщо не є, виконуємо перенаправлення
        return redirect(to='quotes:root')
    
    if request.method == 'POST':
        form = AuthorEditForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:author_detail', author_id=author_id)
    else:
        form = AuthorEditForm(instance=author)
    # тут у словнику [context], ключ - це є сигнатура, яка використовуватиметься в html шаблоні
    return render(request, 'quotes/edit_author.html', {'form': form, 'author': author})


# Ця функцiя для видалення за допомогою кнопки <java-script>
# @login_required
# def delete_quote(request, quote_id):
#     quote = get_object_or_404(Quote, id=quote_id)
#     if request.user.is_authenticated and quote.user == request.user:
#         author = quote.author
#         quote.delete()
        
#         # Перевіряємо, чи є ще цитати автора
#         if Quote.objects.filter(author=author).count() == 0:
#             # Отримуємо об'єкт автора за його ID та видаляємо його
#             author_to_delete = Author.objects.get(id=author.id)
#             author_to_delete.delete()

#         return JsonResponse({'message': 'Your Quote was deleted successfully.'})
#     else:
#         return JsonResponse({'message': 'Your access was not authorized or Quote does not exist.'}, status=401)


@login_required
def delete_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)

    if request.method == 'POST':
        form = DeleteQuoteForm(request.POST)
        # print(type(form["confirm_delete"].value()), form["confirm_delete"].value())
        if request.user.is_authenticated and quote.user == request.user:
            # if form.is_valid() and form['confirm_delete'].value() == "False":
            if form['confirm_delete'].value() == "False":

                # Пользователь подтвердил удаление
                author = quote.author
                quote.delete()
                messages.success(request, 'The Quote deleted successfully.')

                # Перевіряємо, чи є ще цитати автора
                if Quote.objects.filter(author=author).count() == 0:
                    # Отримуємо об'єкт автора за його ID та видаляємо його
                    author_to_delete = Author.objects.get(id=author.id)
                    author_to_delete.delete()

                return redirect(to='quotes:root')
            else:
                messages.warning(request, 'The Quote deletion cancelled')
    else:
        form = DeleteQuoteForm()

    return render(request, 'quotes/delete_quote.html', {'quote': quote, 'form': form})


class TagQuotesView(View):
    template_name = 'quotes/tag_quotes.html'
    quotes_per_page = 10

    def get(self, request, *args, **kwargs):
        # Тут ключ ['tag_name'] тому, що у файлi urls.py заданий шлях <str:tag_name>
        tag_name = kwargs['tag_name']
        tag = Tag.objects.get(name=tag_name)
        quotes_with_tag = Quote.objects.filter(tags=tag)

        paginator = Paginator(list(quotes_with_tag), self.quotes_per_page)
        page = request.GET.get('page')

        try:
            quotes_per_page = paginator.page(page)
        except PageNotAnInteger:
            quotes_per_page = paginator.page(1)
        except EmptyPage:
            quotes_per_page = paginator.page(paginator.num_pages)

        context = {
            'tag_name': tag_name,
            'quotes_with_tag': quotes_per_page,
        }

        return render(request, self.template_name, context)