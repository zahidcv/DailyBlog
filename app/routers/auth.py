
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .. import database, models, schemas, config
from ..config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRATION_MINUTES = settings.access_token_expiration_minutes


router = APIRouter(
    tags=['Authentication']
)

pwd_cxt = CryptContext(schemes=['bcrypt'])
oauth2bearer = OAuth2PasswordBearer(tokenUrl='login')
db_dependency = Annotated[dict, Depends(database.get_db)]

@router.post('/login', status_code=status.HTTP_200_OK)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session = Depends(database.get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    print(user)
    token = create_access_token(user.email, user.id)

    return {'access_token': token, 'token_type': 'bearer'}


def create_access_token(email: str, id: int):
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    encode = {'email': email, 'exp': expires, 'id': id}
         
    return jwt.encode(encode, SECRET_KEY, algorithm = ALGORITHM)

def authenticate_user(email, password, db):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect email')
    
    if not pwd_cxt.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect password')
    
    return user


def get_current_user(token: Annotated[str, Depends(oauth2bearer)], db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email : str = payload.get('email')
        id : int = payload.get('id')
        
        user = db.query(models.User).filter(models.User.id == id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="couldn't validate user")
        
        return user
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWTError, couldn't validate user")