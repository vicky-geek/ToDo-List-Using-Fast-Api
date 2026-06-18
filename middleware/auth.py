from utils.auth import verifyToken
from fastapi import Request, HTTPException

def authenticate(request: Request):
    token = request.headers.get('Authorization').split(' ')[1]
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        user = verifyToken(token)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))