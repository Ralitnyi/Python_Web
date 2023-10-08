from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact
from src.repository import contacts as repository_contacts
from src.schemas import ContactBase, ContactResponse

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_tag(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactBase, contact_id: int, db: Session = Depends(get_db)
):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete(
    "/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    removed_contact = await repository_contacts.remove_contact(contact_id, db)
    if removed_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return removed_contact


@router.get("/search/", response_model=List[ContactResponse])
async def search_contact(
    name: str = Query(None, title="Ім'я контакту", max_length=50),
    last_name: str = Query(None, title="Прізвище контакту", max_length=50),
    email: str = Query(None, title="Email контакту", max_length=50),
    db: Session = Depends(get_db),
) -> List[ContactResponse]:
    contact_responses = await repository_contacts.search_contact(
        name=name, last_name=last_name, email=email, db=db
    )

    return contact_responses


@router.get("/birthday/", response_model=List[ContactResponse])
async def birthday_per_week(db: Session = Depends(get_db)):
    contacts = await repository_contacts.birthday_per_week(db)
    return contacts
