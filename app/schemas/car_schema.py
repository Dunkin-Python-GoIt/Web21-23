from pydantic import BaseModel, Field


class BaseCar(BaseModel):
    brand: str = Field(title="Car brand", min_length=2, max_length=10)
    model: str
    

class CreateCar(BaseCar):
    ...
    

class Car(BaseCar):
    id: int
    
    class Config:
        from_attributes = True