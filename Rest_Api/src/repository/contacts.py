from datetime import datetime, timedelta
from typing import List

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactResponse


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    contacts = (
        db.query(Contact)
        .filter(Contact.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return contacts


async def get_contact(id_: int, user: User, db: Session) -> Contact:
    contact = db.query(Contact).filter_by(id=id_).first()
    return contact


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact:
    print(user.id)
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(
    id_: int, body: ContactBase, user: User, db: Session
) -> Contact:
    contact = db.query(Contact).filter_by(id=id_).first()
    if contact:
        contact.name = body.name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session):
    removed_contact = db.query(Contact).filter_by(id=contact_id).first()
    if removed_contact:
        db.delete(removed_contact)
        db.commit()
    return removed_contact


async def search_contact(
    user: User, db: Session, name: str = None, last_name: str = None, email: str = None
) -> List[ContactResponse]:
    query = db.query(Contact)
    filters = []

    if name:
        filters.append(Contact.name.ilike(f"%{name}%"))
    if last_name:
        filters.append(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        filters.append(Contact.email.ilike(f"%{email}%"))

    contacts = query.filter(or_(*filters)).all()

    # Створіть об'єкт ContactResponse для кожного знайденого контакту
    contact_responses = []
    for contact in contacts:
        contact_response = ContactResponse(
            id=contact.id,
            name=contact.name,
            last_name=contact.last_name,
            email=contact.email,
            phone=contact.phone,
            birthday=contact.birthday,
        )
        contact_responses.append(contact_response)
    return contact_responses


async def birthday_per_week(user: User, db: Session) -> List[Contact]:
    response = []
    today = datetime.today()
    timedelta_now = timedelta(days=0)
    timedelta_end = timedelta(days=7)
    contacts = db.query(Contact).all()
    for contact in contacts:
        if contact.birthday:
            contact_birthday = datetime(
                year=today.year, month=contact.birthday.month, day=contact.birthday.day
            )
            if timedelta_now <= (contact_birthday - today) <= timedelta_end:
                response.append(contact)
    return response
