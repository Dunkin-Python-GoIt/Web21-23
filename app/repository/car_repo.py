from random import randint

from ..schemas import car_schema

async def get_all_cars(db: dict):
    cars = db["cars"]
    return cars

async def create_car(db: dict, car: car_schema.BaseCar):
    id = randint(1, 100)
    raw_car = car.model_dump()
    raw_car["id"] = id
    db["cars"].append(raw_car)
    # new_car = car_schema.Car(**raw_car)
    another_car = {**raw_car}
    another_car["fuel_tank"] = 60
    return another_car