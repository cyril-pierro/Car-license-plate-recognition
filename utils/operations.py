from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.cars import Cars


async def add_car_plate_number(car: str, db: Session):
    new_car = Cars(plate_number=car, status=True)
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


async def get_plate_number(db: Session, plate_number: str):
    car = db.query(Cars).filter(Cars.plate_number == plate_number).first()
    if car:
        return car
    return None
