from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schema, utils
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_users(new_user: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.get_password_hash(new_user.password)  # Updated function name
    new_user.password = hashed_password

    existing_user = db.query(models.User).filter(models.User.email == new_user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    new_user_model = models.User(**new_user.dict())
    db.add(new_user_model)
    db.commit()
    db.refresh(new_user_model)
    return new_user_model

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user_by_id = db.query(models.User).filter(models.User.id == id).first()
    if not user_by_id:
        raise HTTPException(status_code=404, detail=f"User with id: {id} does not exist")
    return user_by_id