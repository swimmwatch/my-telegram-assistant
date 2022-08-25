import random

from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI, Depends

from services.control_panel_api.responses import UsersResponse
from services.control_panel_api.container import ControlPanelApiContainer
from services.db.dal import UserRepository
from services.db.utils import async_init_db

app = FastAPI()
container = ControlPanelApiContainer()


@app.on_event('startup')
async def wire_container():
    container.wire(modules=[__name__])


@app.on_event('startup')
async def init_db():
    await async_init_db(container.db())


@app.get('/api/test')
async def reply_square():
    return {
        'num': random.randint(1, 10) ** 2
    }


@app.get('/api/users', response_model=UsersResponse)
@inject
async def get_all_users(
    user_repo: UserRepository = Depends(Provide[ControlPanelApiContainer.user_repo])
):
    return await user_repo.get_all()
