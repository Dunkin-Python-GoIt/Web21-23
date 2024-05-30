from ipaddress import ip_address

from redis.asyncio import Redis
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from .routers import cars, users
from .settings import settings


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://127.0.0.1:5500",
    "127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

banned_ip = []

@app.middleware("https")
async def ban_ip(request, call_next):
    ip = ip_address(request.client.host)
    print(f"{ip = }")
    if ip in banned_ip:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "You in ban list"})
    response = await call_next(request)
    return response


@app.middleware("https")
async def ban_by_headers(request, call_next):
    headers = request.headers
    print(headers)
    response = await call_next(request)
    return response


app.include_router(cars.router, prefix="/api")
app.include_router(users.router, prefix="/api")

@app.on_event("startup")
async def startup():
    r = await Redis(decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def root():
    return {
        "status": "ok",
        "app_name": settings.app_name
    }