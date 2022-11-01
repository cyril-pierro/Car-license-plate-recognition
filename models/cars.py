from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Cars(Base):
    __tablename__ = "Cars"
    id = Column(Integer, primary_key=True, unique=True)
    plate_number = Column(String(length=200), nullable=False, unique=True)
    status = Column(Boolean(), default=False)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "plate_number": "GC 5463",
                "status": True,
            }
        }
