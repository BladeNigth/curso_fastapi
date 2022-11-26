from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException, status
from app.hashing import Hash
from app.token import create_access_token


def auth_user(usuario, db: Session):

    user = db.query(models.User).filter(models.User.username == usuario.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""No Existe el usuario {usuario.username}, por lo tanto no se puede realizar el Login"""
        )
    if not Hash.verify_password(usuario.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La Contraseña es Incorrecta"
        )
    access_token = create_access_token(
        data={"sub": usuario.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}