# Import necessary modules
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.hashing import Hash
from app import models, schemas


def create(request: schemas.UserBase, db: Session):
    """
    This function creates a new user in the database.

    Args:
        request (schemas.UserBase): The request body containing the user's data.
        db (Session): The database session.

    Returns:
        models.User: The newly created user.
    """
    hashedPassword = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name, email=request.email, password=hashedPassword
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # return {"detail": "User created successfully"}
    return new_user


def get(id: int, db: Session):
    """
    This function returns a single user from the database.

    Args:
        id (int): The id of the user to return.
        db (Session): The database session.

    Raises:
        HTTPException: If the user with the given id is not found.

    Returns:
        models.User: The user with the given id.
    """
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(
            status_code=404, detail=f"User with the id {id} is not available"
        )
    return user.first()