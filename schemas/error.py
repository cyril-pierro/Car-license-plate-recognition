from pydantic import BaseModel


class InvalidImageFormat(BaseModel):
    detail: str = "Invalid image format"
