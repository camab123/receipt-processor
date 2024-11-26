from pydantic import BaseModel, Field
from datetime import date, time
from api.schemas.item import Item

class Receipt(BaseModel):
    __tablename__ = "receipts"
    
    retailer: str = Field(description="The name of the retailer or store the receipt is from.", pattern="^[\\w\\s\\-&]+$", examples=["M&M Corner Market"])
    purchaseDate: date = Field(description="The date the receipt was issued.", example="2021-01-01")
    purchaseTime: time = Field(description="The time the receipt was issued.", example="13:01", pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    items: list[Item] = Field(description="A list of items purchased on the receipt.", min_length=1)
    total: float = Field(description="The total amount paid on the receipt.", example=6.49)

