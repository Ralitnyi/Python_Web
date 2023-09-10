from mongoengine import Document
from mongoengine.fields import BooleanField, StringField


class Contact(Document):
    fullname = StringField()
    email = StringField()
    sent = BooleanField(default=False)
