from fastapi import FastAPI

app = FastAPI()


@app.router("/")
async def root():
    return {"message": "Hello World"}
