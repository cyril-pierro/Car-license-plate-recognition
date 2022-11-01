from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from core.config import tracker
from schemas import cars as p
from schemas import error as e
from utils import operations
from utils.db_context import get_context_db

router = APIRouter()


@router.post(
    "/add_car",
    response_model=p.AddCarOut,
    responses={
        400: {"model": e.InvalidImageFormat},
    },
)
async def add_driver_licence_plate_number(
    base64_image_string: p.CarsIn,
    db: Session = Depends(get_context_db),
) -> dict[str, str]:

    """
    Use this API for adding car licence plate number.
    How to use:
    1. Upload a jpeg or png image or input a base64 string
    2. Click execute
    3. JSON output will be generated with the image labels
    """

    predicted_label = tracker.predict(base64_image_string.base64_image_string)

    if predicted_label == "":
        raise HTTPException(400, "Can't scan Licence plate")

    car = await operations.get_plate_number(plate_number=predicted_label, db=db)

    if car is not None:
        raise HTTPException(400, "car number plate already exist")

    # send payload to client
    registered_car = await operations.add_car_plate_number(
        car=predicted_label, db=db
    )
    predictions: dict[str, str] = {
        "plate_number": registered_car.plate_number,
        "success": "added successfuly",
    }

    return predictions


@router.post(
    "/check_plate_number",
    response_model=p.PredictionOut,
    responses={
        400: {"model": e.InvalidImageFormat},
    },
)
async def check_driver_licence_plate_number(
    base64_image_string: p.CarsIn,
    db: Session = Depends(get_context_db),
) -> dict[str, str]:

    """
    Use this API for detecting car licence plate number.
    How to use:
    1. Upload a jpeg or png image or input a base64 string
    2. Click execute
    3. JSON output will be generated with the image labels
    """

    predicted_label = tracker.predict(base64_image_string.base64_image_string)

    car = await operations.get_plate_number(plate_number=predicted_label, db=db)

    if car is None:
        raise HTTPException(404, "Car number plate not found")

    # send payload to client
    predictions: dict[str, str] = {
        "plate_number": car.plate_number,
        "status": car.status,
    }

    return predictions
