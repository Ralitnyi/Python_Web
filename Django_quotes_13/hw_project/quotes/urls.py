from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("forTag/<int:tag_id>", views.main, name="for_tag"),
    path("addAuthor", views.add_author, name="add_author"),
    path("addQuote", views.add_quote, name="add_quote"),
    path("addTag", views.add_tag, name="add_tag"),
    path("author/<int:author_id>", views.show_author, name="show_author"),
    path("delete/<int:author_id>", views.delete_author, name="delete_author"),
    path("delete_tag/<int:tag_id>", views.delete_tag, name="delete_tag"),
]
