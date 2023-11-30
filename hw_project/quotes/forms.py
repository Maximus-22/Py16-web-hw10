from django import forms
from .models import Quote, Author

# class QuoteForm(forms.ModelForm):
#     class Meta:
#         model = Quote
#         fields = ['quote', 'tags', 'author']

class QuoteForm(forms.ModelForm):
    tags = forms.CharField(max_length=84, help_text="Введіть теги через кому.")

    class Meta:
        model = Quote
        fields = ['quote', 'tags']

    def clean_tags(self):
        # [cleaned_data] -> типу <a box of chocolates> от запроса [POST]
        tags = self.cleaned_data['tags']
        # Розбиваємо рядок з тегами на список, використовуючи кому як роздільник
        return [tag.strip() for tag in tags.split(',')]
    

class AuthorForm(forms.ModelForm):
    fullname = forms.CharField(max_length=64, required=True)
    
    class Meta:
        model = Author
        fields = ['fullname']


class AuthorEditForm(forms.ModelForm):
    born_date = forms.CharField(max_length=64, help_text="Please follow the format: December 25, 2000.")
    born_location = forms.CharField(max_length=256, help_text="Please follow the format: in Florida, USA.")

    class Meta:
        model = Author
        fields = ['born_date', 'born_location', 'description']