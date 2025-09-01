# Import necessary modules
from fastapi import APIRouter, Depends, status
from app import schemas, database, oauth2
from app.repository import blog_repo
from typing import List
from sqlalchemy.orm import Session

# Create a new APIRouter instance
router = APIRouter(prefix="/blog", tags=["Blogs"])


@router.get("/", response_model=List[schemas.ShowBlog])
def all_blogs(
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    """
    This function returns all the blogs from the database.

    Args:
        db (Session, optional): The database session. Defaults to Depends(database.get_db).
        current_user (schemas.User, optional): The current user. Defaults to Depends(oauth2.get_current_user).

    Returns:
        list: A list of all the blogs.
    """
    return blog_repo.all(db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
def create_blog(
    request: schemas.Blog,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    """
    This function creates a new blog in the database.

    Args:
        request (schemas.Blog): The request body containing the blog's data.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).
        current_user (schemas.User, optional): The current user. Defaults to Depends(oauth2.get_current_user).

    Returns:
        models.Blog: The newly created blog.
    """
    return blog_repo.create(request, db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    """
    This function returns a single blog from the database.

    Args:
        id (int): The id of the blog to return.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).
        current_user (schemas.User, optional): The current user. Defaults to Depends(oauth2.get_current_user).

    Returns:
        models.Blog: The blog with the given id.
    """
    return blog_repo.get(id, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    """
    This function deletes a single blog from the database.

    Args:
        id (int): The id of the blog to delete.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).
        current_user (schemas.User, optional): The current user. Defaults to Depends(oauth2.get_current_user).

    Returns:
        Response: A response with a status code of 204.
    """
    return blog_repo.delete(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(
    id: int,
    request: schemas.Blog,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    """
    This function updates a single blog in the database.

    Args:
        id (int): The id of the blog to update.
        request (schemas.Blog): The request body containing the blog's new data.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).
        current_user (schemas.User, optional): The current user. Defaults to Depends(oauth2.get_current_user).

    Returns:
        dict: A dictionary with a detail message.
    """
    return blog_repo.update(id, request, db)
