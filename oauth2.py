import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta, timezone
from schema import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException, Depends
from config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = f'{settings.secret_key}'
ALGORITHM = f'{settings.algorithm}'
ACCESS_TOKEN_EXPIRE_MINUTE = settings.access_token_expire_minutes

def create_access_token(payload: dict):
    payload_to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)

    payload_to_encode.update({'exp': expire})

    jwt_token = jwt.encode(payload_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token

def verify_access_token(token: str, credential_exception):
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = decoded_payload.get('user_id')

        if user_id is None:
            raise credential_exception

        token_data = TokenData(user_id=user_id)

        return token_data
    except PyJWTError:
        raise credential_exception

def get_current_user(token: str = Depends(oauth2_schema)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Couldn\'t validate credentials', headers={
        'WWW-Authenticate': 'Bearer'
    })

    return verify_access_token(token=token, credential_exception=credential_exception)