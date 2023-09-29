from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse
import pydenticon 
from io import BytesIO
import hashlib
import base64

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix='/signup',
    tags=['users']
)

# Defined a dependency to inject the templates variable
def get_templates():
    return Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def get_signup_page(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    # Check if email or username already exists
    existing_user = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.username == user.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email or username already exists. Please use another email or username.')

    # Hash the password
    hashed_password = utils.hash(user.password)

    avatar_generator = pydenticon.Generator(rows=8, columns=8)  # Adjust rows and columns as needed
    avatar_data = avatar_generator.generate(user.email, width=64, height=64)  # Adjust width and height as needed
    
    user_data = user.dict()
    user_data['password'] = hashed_password
    user_data['avatar'] = avatar_data  # Store the avatar data as bytes

    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {'message': 'User created'}