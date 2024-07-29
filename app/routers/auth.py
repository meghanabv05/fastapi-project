from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import schema, models, database, utils
from app.config import settings
from app.routers.oauth2 import create_access_token

router = APIRouter()

@router.post("/login", response_model=schema.Token)
def login(login_data: schema.LoginData, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == login_data.username).first()
    
    if not user or not utils.verify_password(login_data.password, user.password):  # Verify hashed password
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"user_id": user.id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}