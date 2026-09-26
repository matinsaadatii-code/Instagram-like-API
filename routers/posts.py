from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from model import PostModel
from typing import List, Optional
from schema import Post, PostSchemaResponse, TokenData
from oauth2 import get_current_user

router = APIRouter(prefix='/api', tags=['Posts'])

@router.get("/get/posts/{item_id}", response_model=PostSchemaResponse)
def get_post(item_id: int, db: Session = Depends(get_db)):
    try:
        # with connection.cursor() as cursor:
        #     cursor.execute(""" SELECT * FROM public."Posts" WHERE id = %s """, (str(item_id),))
        #     requested_post = cursor.fetchone()

        requested_post = db.query(PostModel).filter(PostModel.id == item_id).first()  

        if requested_post:
            return requested_post
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nothing found! "
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get('/get/posts', status_code=status.HTTP_200_OK, response_model=List[PostSchemaResponse])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search_title_term: Optional[str] = ""):
    try:
        # with connection.cursor() as cursor:
        #     cursor.execute(""" SELECT * FROM public."Posts" """)
        #     posts = cursor.fetchall()

        posts = db.query(PostModel).filter(PostModel.published == True).filter(PostModel.title.contains(search_title_term)).limit(limit).offset(skip).all()

        return posts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get('/get/your/posts', status_code=status.HTTP_200_OK, response_model=List[PostSchemaResponse])
def get_your_posts(db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user), limit: int = 10, skip: int = 0, search_title_term: Optional[str] = ""):
    try:
        # with connection.cursor() as cursor:
        #     cursor.execute(""" SELECT * FROM public."Posts" """)
        #     posts = cursor.fetchall()

        posts = db.query(PostModel).filter(PostModel.user_id == current_user.user_id).filter(PostModel.title.contains(search_title_term)).limit(limit).offset(skip).all() 

        return posts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get('/get/all/posts', status_code=status.HTTP_200_OK, response_model=List[PostSchemaResponse])
def get_all_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search_title_term: Optional[str] = ""):
    try:
        # with connection.cursor() as cursor:
        #     cursor.execute(""" SELECT * FROM public."Posts" """)
        #     posts = cursor.fetchall()

        posts = db.query(PostModel).filter(PostModel.title.contains(search_title_term)).limit(limit).offset(skip).all() 

        return posts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.post('/create/posts', status_code=status.HTTP_201_CREATED, response_model=PostSchemaResponse)
def create_post(post: Post, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        # with connection.cursor() as cursor:
        #     cursor.execute(""" INSERT INTO public."Posts" (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
        #     new_post = cursor.fetchone()
        #     connection.commit()

        new_post = PostModel(user_id=current_user.user_id, **post.dict()) 
        db.add(new_post)
        db.commit() 
        db.refresh(new_post) 

        return new_post
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete('/delete/posts/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(item_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        # with connection.cursor() as cursor:
        #     cursor.execute(""" DELETE FROM public."Posts" WHERE id = %s RETURNING *""", (str(item_id),))
        #     delted_post = cursor.fetchone()
        #     connection.commit()

        deleted_post = db.query(PostModel).filter(PostModel.id == item_id).first() 

        if not deleted_post: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nothing found! "
            )
        else:
            if deleted_post.user_id != current_user.user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not authorized."
                )            
            else:
                db.delete(deleted_post) 
                db.commit()

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.put('/update/posts/{item_id}', status_code=status.HTTP_200_OK)
def update_post(item_id: int, post: Post, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        # with connection.cursor() as cursor:
        #     cursor.execute(""" UPDATE public."Posts" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(item_id),))
        #     updated_post = cursor.fetchone()
        #     connection.commit()

        updated_post_query = db.query(PostModel).filter(PostModel.id == item_id)
        updated_post = updated_post_query.first()
        
        if not updated_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nothing found! "
            )
        else:
            if updated_post.user_id != current_user.user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not authorized."
                )            
            
            updated_post_query.update(post.dict(), synchronize_session=False)
            updated_post = updated_post_query.first()
            db.commit()
            db.refresh(updated_post)

            return updated_post

    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )