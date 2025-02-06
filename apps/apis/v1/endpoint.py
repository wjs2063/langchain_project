
from fastapi import APIRouter, Request

api_router = APIRouter()


@api_router.post("/")
async def generative_api(request: Request):
    return


