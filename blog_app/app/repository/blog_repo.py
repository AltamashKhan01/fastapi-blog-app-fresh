# Import necessary modules
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from app import models, schemas


def all(db: Session):
    """
    This function returns all the blogs from the database.

    Args:
        db (Session): The database session.

    Returns:
        list: A list of all the blogs.
    """
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schemas.Blog, db: Session):
    """
    This function creates a new blog in the database.

    Args:
        request (schemas.Blog): The request body containing the blog's data.
        db (Session): The database session.

    Returns:
        models.Blog: The newly created blog.
    """
    new_blog = models.Blog(
        title=request.title, body=request.body, user_id=request.user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get(id: int, db: Session):
    """
    This function returns a single blog from the database.

    Args:
        id (int): The id of the blog to return.
        db (Session): The database session.

    Raises:
        HTTPException: If the blog with the given id is not found.

    Returns:
        models.Blog: The blog with the given id.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    return blog


def delete(id: int, db: Session):
    """
    This function deletes a single blog from the database.

    Args:
        id (int): The id of the blog to delete.
        db (Session): The database session.

    Raises:
        HTTPException: If the blog with the given id is not found.

    Returns:
        Response: A response with a status code of 204.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    db.delete(blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update(id: int, request: schemas.Blog, db: Session):
    """
    This function updates a single blog in the database.

    Args:
        id (int): The id of the blog to update.
        request (schemas.Blog): The request body containing the blog's new data.
        db (Session): The database session.

    Raises:
        HTTPException: If the blog with the given id is not found.

    Returns:
        dict: A dictionary with a detail message.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    update_data = request.model_dump()
    for key, value in update_data.items():
        setattr(blog, key, value)
    db.commit()
    return {"detail": "Blog updated successfully"}
