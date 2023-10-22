from bson.objectid import ObjectId
from django import template

# from ..utils import get_mongodb
from ..models import Author

register = template.Library()


def get_author(id_):
    # db = get_mongodb() # for MongoDB
    # author = db.authors.find_one({'_id': ObjectId(id_)})

    author = Author.objects.get(pk=id_)
    return author.fullname


register.filter("author", get_author)
