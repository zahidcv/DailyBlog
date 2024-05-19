from typing import Annotated, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import database, models, schemas
from ..database import get_db
from . import auth

router = APIRouter(
    tags=['blogs'],
    prefix="/blog"
)
user_dependency = Annotated[dict, Depends(auth.get_current_user)]


@router.post('/create', status_code=status.HTTP_201_CREATED, )
def create_blog(request:schemas.Blog, current_user: user_dependency, db: Session = Depends(get_db)):
    # print(current_user['id'])
    new_blog = models.Blog(title = request.title, body = request.body, user_id = current_user.id)
    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog
# response_model=list[schemas.ShowBlog],
@router.get("/all", response_model=list[schemas.ShowBlog] )
def blogs(current_user: user_dependency, search:Optional['str']='', limit: int = 10, skip: int = 0, db: Session = Depends(get_db)):

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # print('88888', posts)
    return posts


@router.get("/{id}", response_model=schemas.ShowBlog, )
def blog(id,current_user: user_dependency, db: Session = Depends(get_db)):
    b = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'{id} blog not Found')
    return b

@router.delete('/delete/{id}', )
def delete(id, current_user: user_dependency, db: Session = Depends(get_db)):
    bquery = db.query(models.Blog).filter(models.Blog.id == id)
    b = bquery.first()
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id}Blog not found')
    
    if b.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='It-s not your blog')
    
    
    bquery.delete()
    db.commit()
    return 'deleted'

@router.put('/update/{id}', )
def update(id, current_user: user_dependency, request: schemas.Blog, db: Session = Depends(get_db)):
    b = db.query(models.Blog).filter(models.Blog.id == id)
    if not b.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id}Blog not found')
    
    if b.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='It-s not your blog')
    
    b.update(dict(request))
    db.commit()
    return 'updated'

@router.post('/vote/', )
def vote(vote: schemas.Vote, current_user: user_dependency, db: Session = Depends(get_db)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    
    found_vote = vote_query.first()
    
    if vote.direction == 1:
        if found_vote:
            print("vote found")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='You already voted this post')
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        print('88888888888',new_vote)
        db.add(new_vote)
        db.commit()
        return {'message': "Successfully added vote."}
    
    else:
        if not found_vote:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You havent voted it  this post')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': "Successfully deleted vote."}
    

def add(num1:int, num2:int):
    return num1+num2 