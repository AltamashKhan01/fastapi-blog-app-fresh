# Import the OAuth2PasswordBearer class from the fastapi.security module
from fastapi.security import OAuth2PasswordBearer
# Import the Depends, HTTPException, and status modules from the fastapi module
from fastapi import Depends, HTTPException, status
# Import the verify_token function from the token module
from app.token import verify_token

# Create a new OAuth2PasswordBearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    This function is a dependency that gets the current user from a token.
    It verifies the token and raises an exception if the token is invalid.

    Args:
        token (str, optional): The token to verify. Defaults to Depends(oauth2_scheme).

    Raises:
        credentials_exception: If the token is invalid.

    Returns:
        dict: The user's data.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)