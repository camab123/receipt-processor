from pydantic import BaseModel, Field


class Item(BaseModel):
    __tablename__ = "items"

    shortDescription: str = Field(
        description="The Short Product Description for the item.",
        pattern="^[\\w\\s\\-]+$",
        examples=["Mountain Dew 12PK"],
    )
    price: float = Field(
        description="The total price payed for this item.", examples=[6.49]
    )
