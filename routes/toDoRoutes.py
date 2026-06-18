from fastapi import APIRouter, Depends
from controllers.toDoController1 import (getToDos, addToDo, getToDoById, updateToDoById, deleteToDoById)
from middleware.auth import (authenticate, Authorization)

router = APIRouter(dependencies=[Depends(authenticate), Depends(Authorization)])
router.get('/todos')(getToDos)

router.post('/todos')(addToDo)

router.get('/todo')(getToDoById)
router.put('/todos/{id}')(updateToDoById)
router.delete('/todos/{id}')(deleteToDoById)



#if i want to protect only some routes then what should i do ?

# router = APIRouter()
# router.get('/todos', dependencies=[Depends(authenticate)])(getToDos)
# router.post('/todos', dependencies=[Depends(authenticate)])(addToDo)
# router.get('/todo', dependencies=[Depends(authenticate)])(getToDoById)
# router.put('/todos/{id}', dependencies=[Depends(authenticate)])(updateToDoById)
# router.delete('/todos/{id}', dependencies=[Depends(authenticate)])(deleteToDoById)