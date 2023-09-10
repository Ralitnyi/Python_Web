import json

import connect
import pymongo
from models import Author, Quote


def fill_author(json_file_name):
    with open(json_file_name, "r") as file:
        data = json.load(file)
        for author in data:
            Author(**author).save()


def fill_quotes(json_file_name):
    with open(json_file_name, "r") as file:
        data = json.load(file)
        for quote_data in data:
            author_name = quote_data.get("author")

            author = Author.objects(fullname=author_name).first()

            if author:
                quote = Quote(
                    tags=quote_data.get("tags", []),
                    author=author,
                    quote=quote_data.get("quote", ""),
                )
                quote.save()
            else:
                print(f"Автор з іменем '{author_name}' не знайдений в базі даних.")


if __name__ == "__main__":
    json_file_name = "nosql/author.json"
    fill_author(json_file_name)

    json_file_name = "nosql/quotes.json"
    fill_quotes(json_file_name)
