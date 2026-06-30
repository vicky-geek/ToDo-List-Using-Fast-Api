from pydantic import BaseModel
from fastapi import Response, status
class item(BaseModel):
    id : int
    task: str
    priority: int
    description: str | None = None  # Optional

class ToDo(BaseModel):
    item: item


todo = []


def findIndex(itme):
    for i in range(len(todo)):
        if todo[i].id == itme.id:
            return i
    return -1

def findIndexByID(id):
    print("id => :", id , type(id))
    print("todo => :", todo)
    for i in range(len(todo)):
        if todo[i].id == id:
            return i
    print("index not found")
    return -1

async def getToDos(response: Response):
    print("todo => :", todo,type(todo),type(todo[0]))
    response.status_code = status.HTTP_200_OK
    return {"data": todo}


async def addToDo(ToDo : ToDo,response: Response):
    try:
        print("item :", ToDo.item,type(ToDo.item), "ToDo :", ToDo)

        todo.append(ToDo.item)
        print("id :", todo.index(ToDo.item))    
        # todo[id] = ToDo.item
        response.status_code = status.HTTP_201_CREATED
        return {"id": todo.index(ToDo.item), "item": ToDo.item}
    except Exception as e:
        print("Error :", e)
        return {"error": str(e)}


async def getToDoById(id: int,response: Response):
    try:
        print("id :", id)
        index = findIndexByID(int(id))
        if index == -1:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "ToDo not found"}
        response.status_code = status.HTTP_200_OK
        return todo[index]
    except Exception as e:
        print("Error :", e)
        return {"error": str(e)}

# Path Parameters 
async def updateToDoById(id, ToDo : ToDo,response: Response):
    print("id :", id)
    print("item :", ToDo.item)
    index = findIndexByID(int(id))
    print("index :", index)
    if index == -1:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "ToDo not found"}
    todo[index] = ToDo.item
    response.status_code = status.HTTP_200_OK
    return {"id": id, "item": ToDo.item}


async def deleteToDoById(id: int,response: Response):
    print("id :", id)
    index = findIndexByID(int(id))
    if index == -1:
        response.status_code = status.HTTP_404_NOT_FOUND    
        return {"error": "ToDo not found"}
    del todo[index]
    response.status_code = status.HTTP_200_OK
    return {"message": "ToDo deleted successfully"} 