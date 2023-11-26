from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


from .forms import TagForm, NoteForm
from .models import Tag, Note


# def main(request):
#     return render(request, 'noteapp/index.html')

# def main(request):
#     notes = Note.objects.all()
#     return render(request, 'noteapp/index.html', {"notes": notes})

def main(request):
    notes = Note.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    return render(request, 'noteapp/index.html', {"notes": notes})




# def detail(request, note_id):
#     note = get_object_or_404(Note, pk=note_id)
#     return render(request, 'noteapp/detail.html', {"note": note})

@login_required
def detail(request, note_id):
    # Тепер скрізь при запиті потрiбно додавати умову user = request.user
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'noteapp/detail.html', {"note": note})




# def tag(request):
#     if request.method == 'POST':
#         form = TagForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(to='noteapp:main')
#         else:
#             return render(request, 'noteapp/tag.html', {'form': form})

#     return render(request, 'noteapp/tag.html', {'form': TagForm()})

@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            # Тепер нам потрібно додавати користувача у нотатку та теги, тому процес створення тегу ускладнився.
            # Спочатку ми створюємо тег, але умовою commit=False не зберігаємо його одразу в базу даних. Додаємо
            # користувача до тегу tag.user = request.user і тільки після цього зберігаємо в базу даних tag.save().
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='noteapp:main')
        else:
            return render(request, 'noteapp/tag.html', {'form': form})

    return render(request, 'noteapp/tag.html', {'form': TagForm()})




# def note(request):
#     tags = Tag.objects.all()

#     if request.method == 'POST':
#         form = NoteForm(request.POST)
#         if form.is_valid():
#             new_note = form.save()
#             # тепер до цiєї <notes> потрiбно прив'язати тегi -> <tag>
#             # щоб отримати саме список з елемента форми, ми повинні використовувати метод <getlist>
#             # -> request.POST.getlist('tags')
#             # необхідно використати SQL оператор [IN] для перевірки входження тегу в отриманий список.
#             # Django використовує підхід вказівки імені поля [name], символу подвійного підкреслення і
#             # сам оператор -> filter(name__in=request.POST.getlist('tags'))
#             choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
#             for tag in choice_tags.iterator():
#                 new_note.tags.add(tag)

#             return redirect(to='noteapp:main')
#         else:
#             return render(request, 'noteapp/note.html', {"tags": tags, 'form': form})

#     return render(request, 'noteapp/note.html', {"tags": tags, 'form': NoteForm()})

@login_required
def note(request):
    # Тепер скрізь при запиті потрiбно додавати умову user = request.user
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='noteapp:main')
        else:
            return render(request, 'noteapp/note.html', {"tags": tags, 'form': form})

    return render(request, 'noteapp/note.html', {"tags": tags, 'form': NoteForm()})




# def set_done(request, note_id):
#     Note.objects.filter(pk=note_id).update(done=True)
#     return redirect(to='noteapp:main')

@login_required
def set_done(request, note_id):
    # Тепер скрізь при запиті потрiбно додавати умову user = request.user
    Note.objects.filter(pk=note_id, user=request.user).update(done=True)
    return redirect(to='noteapp:main')




# def delete_note(request, note_id):
#     Note.objects.get(pk=note_id).delete()
#     return redirect(to='noteapp:main')

@login_required
def delete_note(request, note_id):
    # Тепер скрізь при запиті потрiбно додавати умову user = request.user
    Note.objects.get(pk=note_id, user=request.user).delete()
    return redirect(to='noteapp:main')
