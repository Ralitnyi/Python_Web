from django import forms
from django.forms import CharField, ModelForm, TextInput

from .models import Author, Quote, Tag


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=50, required=True, widget=TextInput())
    description = CharField(
        min_length=10, max_length=150, required=True, widget=TextInput()
    )
    born_date = CharField(
        min_length=6,
        max_length=50,
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    born_location = CharField(
        min_length=4, max_length=150, required=True, widget=TextInput()
    )

    class Meta:
        model = Author
        fields = ["fullname", "description", "born_date", "born_location"]


class QuoteForm(ModelForm):
    quote = CharField(min_length=10, max_length=150, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ["quote"]
        exclude = ["tags", "authors"]


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]
