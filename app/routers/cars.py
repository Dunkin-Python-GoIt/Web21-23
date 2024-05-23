from typing import Annotated

from fastapi import APIRouter, Depends

from ..schemas import car_schema
from ..repository import car_repo, auth_repo
from ..databases.db import get_db


router = APIRouter(prefix="/cars")


@router.get("/", response_model=list[car_schema.Car])
async def get_cars(
    _:Annotated[bool, Depends(auth_repo.RoleChecker("user"))],
    db = Depends(get_db)):
    cars = await car_repo.get_all_cars(db)
    return cars


@router.post("/", response_model=car_schema.Car)
async def create_car(
    car:car_schema.BaseCar,
    _:Annotated[bool, Depends(auth_repo.RoleChecker("admin"))],
    db:list = Depends(get_db)):
    new_car = await car_repo.create_car(db, car)
    print(new_car)
    return new_car