# Import the CryptContext class from the passlib.context module
from passlib.context import CryptContext

# Create a new CryptContext instance with the bcrypt scheme
pwd_cxt = CryptContext(schemes=["bcrypt"])


class Hash:
    """
    This class provides methods for hashing and verifying passwords using bcrypt.
    """

    @staticmethod
    def bcrypt(password: str):
        """
        Hashes a password using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(plain_password, hashed_password):
        """
        Verifies a plain password against a hashed password.

        Args:
            plain_password (str): The plain password to verify.
            hashed_password (str): The hashed password to verify against.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return pwd_cxt.verify(plain_password, hashed_password)