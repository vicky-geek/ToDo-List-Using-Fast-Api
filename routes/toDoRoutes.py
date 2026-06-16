from fastapi import APIRouter
from controllers.toDoController1 import (getToDos, addToDo, getToDoById, updateToDoById, deleteToDoById)

router = APIRouter()    # here we can create as toDorouter = APIRouter()
router.get('/todos')(getToDos)

router.post('/todos')(addToDo)

router.get('/todo')(getToDoById)
router.put('/todos/{id}')(updateToDoById)
router.delete('/todos/{id}')(deleteToDoById)
