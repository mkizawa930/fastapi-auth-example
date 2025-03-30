import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.models import Base
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.users import router as user_router
from app.database import engine

Base.metadata.create_all(engine)

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

app.add_middleware(SessionMiddleware, secret_key="secret")

app.include_router(auth_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8001, reload=True)
