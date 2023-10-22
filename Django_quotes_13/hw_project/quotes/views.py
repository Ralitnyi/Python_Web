from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuthorForm, QuoteForm, TagForm
# from .utils import get_mongodb
from .models import Author, Quote, Tag

# Create your views here.


def main(request, tag_id=None, page=1):
    # db = get_mongodb() # for mongodb
    # quotes = db.quotes.find() # for mongodb

    if tag_id:
        tag = get_object_or_404(Tag, id=tag_id)
        quotes = Quote.objects.filter(tags=tag)
        per_page = len(quotes)
    else:
        quotes = Quote.objects.all()
        per_page = 5

    top_tags = Tag.objects.annotate(num_quotes=Count("quote")).order_by("-num_quotes")[
        :10
    ]
    paginator = Paginator(list(quotes), per_page=per_page)
    quotes_on_page = paginator.page(page)
    return render(
        request,
        "quotes/index.html",
        context={"quotes": quotes_on_page, "top_tags": top_tags},
    )


@login_required
def add_author(request):
    authors = Author.objects.all()
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            author.save()
            return redirect(to="quotes:root")
        return render(request, "quotes/author.html", {"form": form})
    return render(
        request,
        "quotes/author.html",
        context={"authors": authors, "form": AuthorForm()},
    )


@login_required
def add_quote(request):
    authors = Author.objects.all()
    tags = Tag.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)

        if form.is_valid():
            quote = form.save()
            author = Author.objects.filter(fullname=request.POST.get("author"))[0]
            quote.author = author
            quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                quote.tags.add(tag)
            return redirect(to="quotes:root")

        return render(
            request,
            "quotes/quote.html",
            {"form": form, "authors": authors, "tags": tags},
        )

    return render(
        request,
        "quotes/quote.html",
        context={"authors": authors, "tags": tags, "form": QuoteForm()},
    )


def show_author(request, author_id):
    author = Author.objects.get(pk=author_id)
    if author:
        return render(request, "quotes/show_author.html", context={"author": author})


@login_required
def delete_author(request, author_id):
    Author.objects.get(pk=author_id).delete()
    return redirect(to="quotes:add_author")


@login_required
def add_tag(request):
    tags = Tag.objects.all()
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            tag.save()
            return redirect(to="quotes:root")
        return render(request, "quotes/tag.html", {"form": form})
    return render(
        request,
        "quotes/tag.html",
        context={"tags": tags, "form": TagForm()},
    )


@login_required
def delete_tag(request, tag_id):
    Tag.objects.get(pk=tag_id).delete()
    return redirect(to="quotes:add_tag")
