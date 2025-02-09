from fastapi import FastAPI
from apis.v1.endpoint import chat_router
from chainlit.utils import mount_chainlit

app = FastAPI()

app.include_router(chat_router)


@app.post("/")
async def root():
    return {"message": "Hello World"}


mount_chainlit(app=app, target="./services/chain_lit_service.py", path="/chainlit")
