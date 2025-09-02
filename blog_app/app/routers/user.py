# Import necessary modules
from fastapi import APIRouter, Depends
from app import schemas, database, oauth2
from app.repository import user_repo
from sqlalchemy.orm import Session

# Create a new APIRouter instance
router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(
    id,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    """
    This function returns a single user from the database.

    Args:
        id (int): The id of the user to return.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).
        current_user (schemas.User, optional): The current user. Defaults to Depends(oauth2.get_current_user).

    Returns:
        models.User: The user with the given id.
    """
    return user_repo.get(id, db)


@router.put("/{id}", status_code=202)
def update_user(
    id: int,
    request: schemas.UserBase,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return user_repo.update(id, request, db)


@router.delete("/{id}", status_code=204)
def delete_user(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return user_repo.delete(id, db)
