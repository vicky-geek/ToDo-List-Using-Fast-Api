from fastapi import APIRouter
from controllers.authController import (register,login)

router = APIRouter()    # here we can create as toDorouter = APIRouter()
router.post('/register')(register)

router.post('/login')(login)