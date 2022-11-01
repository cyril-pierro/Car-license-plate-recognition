from pydantic import BaseModel


class CarsIn(BaseModel):
    base64_image_string: str


class PredictionOut(BaseModel):
    plate_number: str
    status: bool

    class Config:
        schema_extra = {"example": {"plate_number": "GC 3456", "status": "True"}}


class AddCarOut(BaseModel):
    plate_number: str
    success: str

    class Config:
        schema_extra = {
            "example": {"plate_number": "GC 3456", "success": "added successfully"}
        }
