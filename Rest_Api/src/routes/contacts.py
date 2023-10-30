from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact, User
from src.repository import contacts as repository_contacts
from src.schemas import ContactBase, ContactResponse
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get(
    "/",
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def list_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    current_user: User = Depends(auth_service.get_current_user),
) -> list[ContactResponse] | ContactResponse:
    """
    The list_contacts function returns a list of contacts.
    
    :param skip: int: Skip the first n contacts
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Get the database connection
    :param first_name: str: Filter contacts by first name
    :param last_name: str: Filter the contacts by last name
    :param email: str: Filter the contacts by email
    :param current_user: User: Get the current user from the database
    :param : Get the current user
    :return: A list of contactresponse objects, but the get_contact function returns a single contactresponse object
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)

    if first_name:
        contacts = await repository_contacts.get_contact_by_first_name(
            first_name, current_user, db
        )
    elif last_name:
        contacts = await repository_contacts.get_contact_by_last_name(
            last_name, current_user, db
        )
    elif email:
        contacts = await repository_contacts.get_contact_by_email(
            email, current_user, db
        )

    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no contacts"
        )

    return contacts


@router.post(
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    description="No more than 2 requests per minute",
    dependencies=[Depends(RateLimiter(times=2, seconds=60))],
)
async def create_contact(
    body: ContactBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_contact function creates a new contact in the database.
        The function takes in a ContactBase object, which is defined as follows:
            class ContactBase(ContactInDB):
                id: int
                name: str
                email_address: str = None
    
    :param body: ContactBase: Get the contact details from the request body
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user that is currently logged in
    :param : Get the current user from the database
    :return: The contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.create_contact(body, current_user, db)
    return contact


@router.get("/birthday", response_model=list[ContactResponse])
async def get_birthday(
    interval: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_birthday function returns a list of contacts with birthdays in the next 7 days.
    
    :param interval: int: Specify the number of days from today to search for birthdays
    :param db: Session: Get the database session
    :param current_user: User: Get the user id from the token
    :param : Define the number of days in which we want to get birthdays
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts_by_birthday(
        interval, current_user, db
    )
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"In the next {interval} days there are no birthdays.",
        )
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_contact function returns a contact by its id.
    
    :param contact_id: int: Get the contact by id
    :param db: Session: Get the database session
    :param current_user: User: Get the user from the database
    :param : Get the contact id from the url
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactBase,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            - body: A ContactBase object containing the new values for the contact.
            - contact_id: An integer representing the id of an existing contact to be updated.
            - db (optional): A Session object used to connect to and query a database, defaults to None if not provided by caller. 
                If no db is provided, one will be created using get_db().
    
    :param body: ContactBase: Receive the data from the request body
    :param contact_id: int: Identify the contact to be updated
    :param db: Session: Get the database session
    :param current_user: User: Get the user id of the logged in user
    :param : Get the contact id from the url
    :return: A contactbase object
    :doc-author: Trelent
    """
    new_contact = await repository_contacts.update_contact(
        body, contact_id, current_user, db
    )
    if not new_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return new_contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The delete_contact function deletes a contact from the database.
        Args:
            contact_id (int): The id of the contact to delete.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): User object for currently logged in user. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_id: int: Specify the contact id that will be deleted
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :param : Get the contact id
    :return: The deleted contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.delete_contact(contact_id, current_user, db)
    return contact
