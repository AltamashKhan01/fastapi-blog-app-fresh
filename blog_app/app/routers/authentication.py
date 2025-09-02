# Import necessary modules
from fastapi import APIRouter, Depends, HTTPException, status
from app import database, models, token, schemas
from app.repository import user_repo
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.hashing import Hash

# Create a new APIRouter instance
router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    """
    This function logs in a user.

    Args:
        request (OAuth2PasswordRequestForm, optional): The request body containing the user's credentials. Defaults to Depends().
        db (Session, optional): The database session. Defaults to Depends(database.get_db).

    Raises:
        HTTPException: If the user's credentials are invalid.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials",
        )
    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", status_code=201, response_model=schemas.ShowUser)
def register(request: schemas.UserBase, db: Session = Depends(database.get_db)):
    """
    This function creates a new user in the database.

    Args:
        request (schemas.UserBase): The request body containing the user's data.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).

    Returns:
        models.User: The newly created user.
    """
    return user_repo.create(request, db)
