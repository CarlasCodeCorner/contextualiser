from app.models.User import User
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

JWT_SECRET = 'Some_Key'
ALGORITHMUS = 'HS256'

pwd_context = CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_password_hash(password: str) -> str:
    """generates hash password from plain password

    Args:
        password (str): plain password

    Returns:
        _type_: hashed password using bcrypt
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """verifies if plain password is the generated hashed password

    Args:
        plain_password (str): _description_
        hashed_password (str): _description_

    Returns:
        _type_: true if plain password equals hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)

##TODO delete Token with an expiration DATE

def create_access_token(user: User) -> str:
    """create an JWT based on  username, email and role

    Args:
        user (User): User model

    Returns:
        _type_: json web token: representation of header, claims and signature
    """
    claims = {
        'sub': user.username,
        'email': user.email,
        'role': user.dict()['role']
    }
    return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=ALGORITHMUS)

def decode_token(token: str = Depends(oauth2_scheme)):
    """decodes a token based on JWT

    Args:
        token (str, optional): JWT. Defaults to Depends(oauth2_scheme).

    Returns:
        _type_: decoded claim
    """
    claims = jwt.decode(token, key=JWT_SECRET)
    return claims

def check_role(claims: dict = Depends(decode_token)):
    """check if admin is 

    Args:
        claims (dict, optional):oken). decoded jwt

    Raises:
        HTTPException:

    Returns:
        _type_: decoded claim
    """
    role = claims['role'][0]['role']
    if role == 'admin' or role == 'user':
        return claims
    else:
        raise HTTPException(status_code=403, detail='JWT token could not be verified')
    


def check_admin(claims: dict = Depends(decode_token)):
    """check if admin is 

    Args:
        claims (dict, optional):oken). decoded jwt

    Raises:
        HTTPException:

    Returns:
        _type_: decoded claim
    """
    role = claims['role'][0]['role']
    if role != 'admin':
        raise HTTPException(status_code=403, detail='Only Admins allowed')
    return claims


