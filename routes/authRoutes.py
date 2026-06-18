from fastapi import APIRouter
from controllers.authController import (register,login,logout,refreshToken)

router = APIRouter()    # here we can create as toDorouter = APIRouter()
router.post('/register')(register)

router.post('/login')(login)

router.get('/logout')(logout)

router.post('/refresh-token')(refreshToken)