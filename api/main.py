import uvicorn
from fastapi import Depends, FastAPI

from api import schemas, models
from api.database import engine
from api.routers.auth import router as auth_router
from api.routers.users import router as user_router

models.Base.metadata.create_all(engine)

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8001, reload=True)
