from fastapi import Depends, Request, HTTPException, status

from utils.auth import verifyToken
from utils.constant import ROLE_PERMISSIONS


def authenticate(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    token = auth_header.split(" ", 1)[1]
    print("token :", token)
    user = verifyToken(token)
    print("user :", user)
    request.state.user = user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return user


def _get_allowed_methods(path: str, allowed_paths: dict) -> list | None:
    if path in allowed_paths:
        return allowed_paths[path]
    for allowed_path, methods in allowed_paths.items():
        if path.startswith(f"{allowed_path}/"):
            return methods
    return None


def Authorization(request: Request):
    print("request.state.user :", request.state.user)
    auth_header = request.headers.get("Authorization")
    accessToken = auth_header.split(" ", 1)[1]
    if not accessToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    user = verifyToken(accessToken)
    role = user.get("role")
    path = request.url.path
    method = request.method
    allowed_paths = ROLE_PERMISSIONS.get(role, {})
    allowed_methods = _get_allowed_methods(path, allowed_paths) or []
    print("role :", role)
    print("path :", path)
    print("allowed_paths :", allowed_paths)
    print("allowed_methods :", allowed_methods)
    print("method :", method)
    if allowed_methods is None or not allowed_methods:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    if method not in allowed_methods:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    return user

def AuthorizationWithAuthentication(request: Request,user: dict = Depends(authenticate)):
    role = user.get("role")
    path = request.url.path
    method = request.method
    allowed_paths = ROLE_PERMISSIONS.get(role, {})
    allowed_methods = _get_allowed_methods(path, allowed_paths) or []
    print("role :", role)
    print("path :", path)
    print("allowed_paths :", allowed_paths)
    print("allowed_methods :", allowed_methods)
    print("method :", method)
    if allowed_methods is None or not allowed_methods:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    if method not in allowed_methods:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    return user