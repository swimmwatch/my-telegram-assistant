import random
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, FastAPI

from services.control_panel_api.container import ControlPanelApiContainer
from services.control_panel_api.schemas.user import User
from services.db.dal import UserRepository
from services.db.utils import async_init_db

app = FastAPI()
container = ControlPanelApiContainer()


@app.on_event("startup")
async def wire_container():
    container.wire(modules=[__name__])


@app.get("/api/test")
async def reply_square():
    return {"num": random.randint(1, 10) ** 2}


@app.get("/api/users", response_model=List[User])
@inject
async def get_all_users(
    user_repo: UserRepository = Depends(Provide[ControlPanelApiContainer.user_repo]),
):
    users = await user_repo.get_all()
    return [User(id=user.id, name=user.name) for user in users]
