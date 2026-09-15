from fastapi import status, HTTPException, Depends, APIRouter
from database import get_db
from sqlalchemy.orm import Session
from schema import UserLogin, Token
from model import UserModel
from utils import verify_password
from oauth2 import create_access_token

router = APIRouter(tags=['Auth'])

@router.post('/login', response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_login.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        ) 
    if not verify_password(user_login.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        ) 

    access_token = create_access_token(payload={
        'user_id': user.id
    })

    return {'access_token': access_token, 'token_type': 'bearer'}

