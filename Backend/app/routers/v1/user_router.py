from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.database import crud, schemas, models
from app.database.database import get_db
from app.utils.verify import verify_password
from app.utils.oauth2 import create_access_token, get_current_user
from app.common.config import ACCESS_TOKEN_EXPIRES_IN

router = APIRouter(
    prefix="/api/v1/user",
)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_existing_user(db=db, user_create=user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already exists.")
    crud.create_user(db=db, user_create=user_create)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Email or Password",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Email or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "status": "success",
        "access_token": access_token,
        "access_token_expires_in": ACCESS_TOKEN_EXPIRES_IN * 60,
        "is_admin": user.is_admin,
    }


@router.get("/me", response_model=schemas.User)
def get_user_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.get("/all", response_model=schemas.UserList)
def get_all_users(skip: int, limit: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource."
        )

    return crud.get_users(db=db, skip=skip, limit=limit)


@router.get("/{user_id}/get", response_model=schemas.User)
def get_user_me(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource."
        )

    db_User: models.User = crud.get_user_by_id(db=db, id=user_id)

    if not db_User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return db_User


@router.put("/{user_id}/update", status_code=status.HTTP_204_NO_CONTENT)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource."
        )

    db_user: models.User = db.query(models.User).filter(
        models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    db_user.name = user_update.name or db_user.name
    db_user.phone = user_update.phone or db_user.phone
    db_user.birth = user_update.birth or db_user.birth
    db_user.email_enable = user_update.email_enable or db_user.email_enable
    db_user.first_judging_permission = user_update.first_judging_permission or db_user.first_judging_permission
    db_user.second_judging_permission = user_update.second_judging_permission or db_user.second_judging_permission
    db.commit()
