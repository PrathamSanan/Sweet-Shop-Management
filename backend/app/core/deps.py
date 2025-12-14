from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.core.jwt import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("sub") is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        return payload   # 🔥 IMPORTANT

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User


def get_admin_user(
    user=Depends(get_current_user)
):
    if not user.get("is_admin"):
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return user
