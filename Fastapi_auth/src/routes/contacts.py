from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact, User
from src.repository import contacts as repository_contacts
from src.schemas import ContactBase, ContactResponse
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get('/')
async def list_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        first_name: str = None, last_name: str = None, email: str = None,
                        current_user: User = Depends(auth_service.get_current_user)
                        ) -> list[ContactResponse] | ContactResponse:
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)

    if first_name:
        contacts = await repository_contacts.get_contact_by_first_name(first_name, current_user, db)
    elif last_name:
        contacts = await repository_contacts.get_contact_by_last_name(last_name, current_user, db)
    elif email:
        contacts = await repository_contacts.get_contact_by_email(email, current_user, db)

    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no contacts")

    return contacts


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create_contact(body, current_user, db)
    return contact


@router.get('/birthday', response_model=list[ContactResponse])
async def get_birthday(interval: int = 7, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts_by_birthday(interval, current_user, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"In the next {interval} days there are no birthdays.")
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse)
async def get_contact(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact


@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    new_contact = await repository_contacts.update_contact(body, contact_id, current_user, db)
    if not new_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return new_contact


@router.delete('/{contact_id}', response_model=ContactResponse)
async def delete_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.delete_contact(contact_id, current_user, db)
    return contact
