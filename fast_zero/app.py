from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, PublicUser, UserDB, UserList, UserSchema

app = FastAPI()

database = []


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo'}


@app.get('/users/', response_model=UserList, status_code=HTTPStatus.OK)
def read_users():
    return {'users': database}


@app.get('/users/{user_id}', response_model=PublicUser)
def read_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not Found'
        )
    return database[user_id - 1]


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=PublicUser)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)

    return user_with_id


@app.put('/users/{user_id}', response_model=PublicUser)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not Found'
        )
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not Found'
        )
    del database[user_id - 1]
    return {'message': 'User Deleted'}
