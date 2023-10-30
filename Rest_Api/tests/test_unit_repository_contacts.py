import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session
from datetime import datetime

from src.schemas import ContactBase, ContactResponse
from src.database.models import Contact, User
from src.repository.contacts import (
    get_contact,
    get_contacts,
    create_contact,
    remove_contact,
    search_contact,
    update_contact,
    birthday_per_week,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.contact = Contact(id=1, name='test_Ivan', email='test email', phone='0999999999')
        self.contacts = [self.contact,
                        Contact(id=2, name=self.contact.name, last_name=None, email='test_email', phone='test_phone', birthday=datetime(2007, 10, 30)),
                        Contact(id=3, name=self.contact.name, last_name=None, email='test_email', phone='test_phone', birthday=datetime(2006, 10, 29))
                        ]

    
    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(0, 10, User(), self.session)
        self.assertListEqual(result, contacts)

    
    async def test_get_contact(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact(0, User(), self.session)
        self.assertEqual(result, contact)

    
    async def test_get_contact_not_found(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = None
        result = await get_contact(0, User(), self.session)
        self.assertIsNone(result)

    
    async def test_create_contact(self):
        body = ContactBase(
            name=self.contact.name,
            last_name='Test R',
            email='Test email',
            phone='0999999999',
            birthday=None,
            description='Test description',
        )
        result = await create_contact(body, User(), self.session)
        self.assertEqual(result.name, self.contact.name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "id"))

    
    async def test_update_contact_found(self):
        body = ContactBase(name=self.contact.name,
                           last_name=None,
                           email=self.contact.email,
                           phone=self.contact.phone,
                           birthday=None)
        self.session.query().filter_by().first.return_value = self.contact
        self.session.commit.return_value = None
        result = await update_contact(id_=1, body=body, user=User(), db=self.session)
        self.assertEqual(result, self.contact)
        
    
    async def test_update_contact_not_found(self):
        self.session.query().filter_by().first.return_value = None
        result = await update_contact(1, ContactBase, User(), db=self.session)
        self.assertIsNone(result)

    
    async def test_remove_contact(self):
        self.session.query().filter_by().first.return_value = self.contact
        result = await remove_contact(1, User(), self.session)
        self.assertEqual(result, self.contact)

    
    async def test_remove_contact_not_found(self):
        self.session.query().filter_by().first.return_value = None
        result = await remove_contact(1, User(), self.session)
        self.assertIsNone(result, 'db returned object')

    
    async def test_search_contact(self):
        contacts = [self.contact, Contact(id=2, name=self.contact.name, last_name=None, email='test_email', phone='test_phone', birthday=None)]
        query = self.session.query.return_value
        query.filter().all.return_value = contacts
        response_contacts = [ContactResponse(
            id=contact.id,
            name=contact.name,
            email=contact.email,
            phone=contact.phone,
            last_name=contact.last_name,
            birthday=contact.last_name) for contact in contacts]
        result = await search_contact(User(), db=self.session, name=self.contact.name)
        self.assertListEqual(result, response_contacts)

    
    async def test_birthday_per_week(self):
        self.session.query().all.return_value = self.contacts
        result = await birthday_per_week(User(), self.session)
        list_birthdays = [self.contacts[1], self.contacts[2]]
        self.assertListEqual(result, list_birthdays)

    
if __name__ == "__main__":
    unittest.main()