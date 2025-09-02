# Import necessary modules for handling dates, times, and JWTs.
from datetime import datetime, timedelta, timezone
from app.schemas import TokenData
from jose import JWTError, jwt
import secrets

# Configuration for JWT token generation.
# It's crucial to keep the SECRET_KEY secure and not expose it publicly.
# In a production environment, this should be loaded from a secure configuration source.
SECRET_KEY = secrets.token_urlsafe(32)
# The algorithm used to sign the JWT.
ALGORITHM = "HS256"
# The duration for which the access token is valid, in minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(data: dict):
    """
    Generates a JWT access token.

    Args:
        data: A dictionary containing the payload to be encoded in the token.
              This typically includes user identification information.

    Returns:
        An encoded JWT string.
    """
    to_encode = data.copy()
    # Calculate the token's expiration time.
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Add the expiration time to the payload.
    to_encode.update({"exp": expire})
    # Encode the complete payload into a JWT.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Verifies the integrity and validity of a JWT token.

    Args:
        token: The JWT token to be verified.
        credentials_exception: The exception to raise if token verification fails.

    Raises:
        credentials_exception: If the token is invalid, expired, or does not
                               contain the required payload data.

    Returns:
        A TokenData object containing the payload's subject (email) if verification is successful.
    """
    try:
        # Attempt to decode the token using the secret key and algorithm.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract the subject ('sub') claim, which should be the user's email.
        email = payload.get("sub")
        if email is None:
            # If the subject is missing, the token is invalid.
            raise credentials_exception
        # Create a TokenData object for validated data.
        token_data = TokenData(email=email)
    except JWTError:
        # If any error occurs during decoding (e.g., signature mismatch, expired token),
        # raise the provided exception.
        raise credentials_exception
    return token_data

