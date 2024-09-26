from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models.user import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix='/user', tags = ['user'])

@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users_all = db.scalar(select(User).where(User.id == True)).all()
    return users_all

@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)],user_id: int):
    users_search = db.scalar(select(User).where(User.id == user_id))
    if users_search is None:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = 'User was not found'
        )
    return users_search

@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age))
    db.commit()
    return {
        'status code:': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    user_upd = db.scalar(select(User).where(User.id == user_id))
    if user_upd is None:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = 'User was not found'
        )
    db.execute(update(User).values(username=update_user.username,
                                   firstname=update_user.firstname,
                                   lastname=update_user.lastname,
                                   age=update_user.age))
    db.commit()
    return {
        'status code:': status.HTTP_201_CREATED,
        'transaction': 'User update is successful!'
    }

@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_del = db.scalar(select(User).where(User.id == user_id))
    if user_del is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status code:': status.HTTP_201_CREATED,
        'transaction': 'User delete'
    }