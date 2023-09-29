
from io import BytesIO
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from jose import JWTError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse

from .. import main, models, schemas, utils
from ..database import get_db

from ..routers import auth

router = APIRouter(
    tags=['analyze']
)  



def get_templates():
    return Jinja2Templates(directory="app/templates")

@router.get("/dashboard/", response_class=HTMLResponse)
async def get_dashboard_page(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("dashboard.html", {"request": request})
@router.get("/", response_class=HTMLResponse)
async def get_index_page(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/dashboard/user/avatar", response_class=HTMLResponse)
async def get_dashboard_user_avatar(current_user: int = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == current_user).first()
        if not user or not user.avatar:
            return {"message": "User or avatar not found"}, 404

        return StreamingResponse(BytesIO(user.avatar), media_type="image/png")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate token")
    
@router.get("/user/profile", response_class=HTMLResponse)
async def get_profile(current_user: int = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == current_user).first()
        data = schemas.UserDetails(username=user.username, email=user.email)
        return JSONResponse(content=data.dict(), status_code=status.HTTP_200_OK)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
      

