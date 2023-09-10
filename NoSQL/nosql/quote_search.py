import connect
from models import Author, Quote


def indexerror_decor(func):
    def inner(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
        except IndexError:
            return []
        return r

    return inner


@indexerror_decor
def search_name(value):
    value = " ".join(value.split(" ")[1:])
    author = Author.objects(fullname=value).first()
    if author:
        quotes = Quote.objects(author=author.id)
        return quotes
    return []


@indexerror_decor
def search_tag(value: str) -> list:
    if not value:
        return []
    content = value.split(" ")[1:]
    content = content[0].split(",")
    quotes = Quote.objects(tags__in=[*content])
    return quotes


def pretty_show(objects_list):
    result = ""
    for obj in objects_list:
        obj_dict = obj.to_mongo().to_dict()

        for key, val in obj_dict.items():
            result += f'"{key}": {val}\n'
        result += "---------------------------\n"
    return result


while True:
    entry = input("format (name|tag: content)\nEnter command >>>")

    if entry.startswith("name:"):
        objects_list = search_name(entry)
        result = pretty_show(objects_list)
        print(result)

    elif entry.startswith("tag:"):
        objects_list = search_tag(entry)
        result = pretty_show(objects_list)
        print(result)

    elif entry == "exit":
        print("END")
        break

    else:
        print("Nothing was found")
