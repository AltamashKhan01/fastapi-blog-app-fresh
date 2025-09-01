# Import necessary modules
from fastapi import APIRouter, Depends
from app import schemas, database, oauth2
from app.repository import user_repo
from sqlalchemy.orm import Session

# Create a new APIRouter instance
router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/", status_code=201, response_model=schemas.ShowUser)
def create_user(
    request: schemas.UserBase,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    """
    This function creates a new user in the database.

    Args:
        request (schemas.UserBase): The request body containing the user's data.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).
        current_user (schemas.User, optional): The current user. Defaults to Depends(oauth2.get_current_user).

    Returns:
        models.User: The newly created user.
    """
    return user_repo.create(request, db)


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
