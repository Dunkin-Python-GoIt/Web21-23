from fastapi import FastAPI

from .routers import cars, users

app = FastAPI()

app.include_router(cars.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.get("/")
async def root():
    return {
        "status": "ok"
    }