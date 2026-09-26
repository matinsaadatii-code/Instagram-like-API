from typing import List, Optional
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from model import UserModel
from schema import UserSchema, UserSchemaResponse, TokenData
from sqlalchemy.orm import Session
from utils import hash_password
from oauth2 import get_current_user

router = APIRouter(prefix="/api", tags=["Users"])

@router.get("/get/users/{item_id}", response_model=UserSchemaResponse)
def get_user(item_id: int, db: Session = Depends(get_db)):
    try:
        requested_user = (
            db.query(UserModel).filter(UserModel.id == item_id).first()
        )

        if requested_user:
            return requested_user  
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Nothing found!"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )

@router.get(
    "/get/users",
    status_code=status.HTTP_200_OK,
    response_model=List[UserSchemaResponse],
)
def get_users(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search_email_term: Optional[str] = ""):
    try:
        users = db.query(UserModel).filter(UserModel.email.contains(search_email_term)).limit(limit).offset(skip).all()
        return users  
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )

@router.post(
    "/create/users",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchemaResponse,
)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    try:
        user.password = hash_password(user.password)
        new_user = UserModel(**user.dict()) 
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user  
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )

@router.delete(
    "/delete/users/{item_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(item_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        deleted_user = (
            db.query(UserModel).filter(UserModel.id == item_id).first()
        )

        if not deleted_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Nothing found!"
            )
        if deleted_user.user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized."
            ) 

        db.delete(deleted_user)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )


@router.put("/update/user/{item_id}", response_model=UserSchemaResponse)
def update_user(
    item_id: int, user: UserSchema, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)
):
    try:
        updated_user_query = db.query(UserModel).filter(UserModel.id == item_id)
        updated_user = updated_user_query.first()

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Nothing found!"
            )
        if updated_user.user_id != current_user.user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not authorized."
                ) 

        updated_user_query.update(user.dict(), synchronize_session=False)
        db.commit()
        db.refresh(updated_user)

        return updated_user  
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )