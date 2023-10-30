from datetime import datetime, timedelta
from typing import List

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactResponse


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.
        
    
    :param skip: int: Skip the first n contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = (
        db.query(Contact)
        .filter(Contact.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return contacts


async def get_contact(id_: int, user: User, db: Session) -> Contact:
    """
    The get_contact function returns a contact from the database.
        Args:
            id_ (int): The ID of the contact to be retrieved.
            user (User): The user who is requesting this information.
            db (Session): A connection to the database, which will be used for querying and updating data.
    
    :param id_: int: Specify the id of the contact to be retrieved
    :param user: User: Get the user who is making the request
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(id=id_).first()
    return contact


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.
        
    
    :param body: ContactBase: Pass in the contact details
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    print(user.id)
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(
    id_: int, body: ContactBase, user: User, db: Session
) -> Contact:
    """
    The update_contact function updates a contact in the database.
        Args:
            id_ (int): The ID of the contact to update.
            body (ContactBase): The updated information for the contact.
            user (User): The current user, used to check if they are authorized to update this contact.
            db (Session): A connection with an open transaction, used for querying and updating data.
    
    :param id_: int: Get the id of the contact to be updated
    :param body: ContactBase: Get the data from the request body
    :param user: User: Get the user information from the token
    :param db: Session: Interact with the database
    :return: The updated contact
    :doc-author: Trelent
    """
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
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact.
            db (Session): A session object for interacting with our database.
    
    :param contact_id: int: Identify the contact to be removed
    :param user: User: Identify the user who is making the request
    :param db: Session: Access the database
    :return: The removed contact object
    :doc-author: Trelent
    """
    removed_contact = db.query(Contact).filter_by(id=contact_id).first()
    if removed_contact:
        db.delete(removed_contact)
        db.commit()
    return removed_contact


async def search_contact(
    user: User, db: Session, name: str = None, last_name: str = None, email: str = None
) -> List[ContactResponse]:
    """
    The search_contact function searches for contacts in the database.
    
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :param name: str: Search for a contact by name
    :param last_name: str: Filter the contacts by last name
    :param email: str: Filter the contacts by email
    :return: A list of contactresponse objects
    :doc-author: Trelent
    """
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
    """
    The birthday_per_week function returns a list of contacts whose birthday is within the next 7 days.
    
    
    :param user: User: Pass the user's information to the function
    :param db: Session: Access the database
    :return: A list of contacts whose birthday is in the next 7 days
    :doc-author: Trelent
    """
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
