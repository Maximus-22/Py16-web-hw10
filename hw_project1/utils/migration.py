import os
import django

from pymongo import MongoClient


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_project.settings")
django.setup()

from quotes.models import Author, Quote, Tag

# виконання
# py -m utils.migration


client = MongoClient("mongodb+srv://maximusm_22:<password>@cluster0.aemcehc.mongodb.net/")
# client = MongoClient("mongodb://localhost")
db = client["BD-homework"]

# authors_db = db.authors.find()

# for author in authors_db:
#     Author.objects.get_or_create(
#         fullname = author["fullname"],
#         born_date = author["born_date"],
#         born_location = author["born_location"],
#         description = author["description"],
#     )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote["tags"]:
        # print(tag) # тут кортежiв немає, але все одно обрiзаємо їх
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)
    
    # страхування вiд повторного заповнення даних -> заповнюємо, коли <quote> не iснує
    # bool(len(0)) -> False
    exist_quote = bool(len(Quote.objects.filter(quote=quote["quote"])))
    if not exist_quote:
        # в database MongoDB знаходимо автора за <id>
        # quote["author"] -> id, <"_id"> = id
        author = db.authors.find_one({"_id": quote["author"]})
        # тепер певний автор спiвставляється по <fullname> з database SQL
        a = Author.objects.get(fullname=author["fullname"])
        q = Quote.objects.create(quote=quote["quote"], author = a, user_id=None)
        
        for tag in tags:
            q.tags.add(tag)