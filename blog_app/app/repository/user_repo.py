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


def update(id: int, request: schemas.UserBase, db: Session):
    """
    This function updates a user in the database.

    Args:
        id (int): The id of the user to update.
        request (schemas.UserBase): The request body containing the updated user's data.
        db (Session): The database session.

    Raises:
        HTTPException: If the user with the given id is not found.

    Returns:
        models.User: The updated user.
    """
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(
            status_code=404, detail=f"User with the id {id} is not available"
        )

    hashedPassword = Hash.bcrypt(request.password)
    user.update(
        {
            models.User.name: request.name,
            models.User.email: request.email,
            models.User.password: hashedPassword,
        }
    )
    db.commit()
    return {"detail": "User updated successfully"}


def delete(id: int, db: Session):
    """
    This function deletes a user from the database.

    Args:
        id (int): The id of the user to delete.
        db (Session): The database session.

    Raises:
        HTTPException: If the user with the given id is not found.

    Returns:
        dict: A message indicating that the user was deleted successfully.
    """
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(
            status_code=404, detail=f"User with the id {id} is not available"
        )
    user.delete(synchronize_session=False)
    db.commit()
    return {"detail": "User deleted successfully"}
