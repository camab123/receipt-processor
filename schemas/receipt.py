from datetime import date, time

from pydantic import BaseModel, Field

from schemas.item import Item


class Receipt(BaseModel):
    __tablename__ = "receipts"

    retailer: str = Field(
        description="The name of the retailer or store the receipt is from.",
        pattern="^[\\w\\s\\-&]+$",
        examples=["M&M Corner Market"],
    )
    purchaseDate: date = Field(
        description="The date the receipt was issued.", example="2021-01-01"
    )
    purchaseTime: time = Field(
        description="The time the receipt was issued.",
        example="13:01",
        pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$",
    )
    items: list[Item] = Field(
        description="A list of items purchased on the receipt.", min_length=1
    )
    total: float = Field(
        description="The total amount paid on the receipt.", example=6.49
    )

    def get_points(self) -> int:
        """Calculate the points for the given receipt"""
        points = 0
        # Count of alphanumeric characters in the retailer name
        points += self.alphanumeric_count(self.retailer)
        # Check if the total is a round number
        points += 50 if self.total.is_integer() else 0
        # Add points for every 2 items purchased
        points += len(self.items) // 2 * 5
        # Add points if trimmed 
        points += self.get_trimmed_description_value()
        # Add points if the day of purchase is odd
        points += 6 if self.is_day_of_purchase_odd() else 0
        # Add points if the purchase time is between 2pm and 4pm
        points += 10 if self.is_time_between_range() else 0

        return points

    
    def alphanumeric_count(value: str):
        return sum(char.isalnum() for char in value)
    
    def get_trimmed_description_value(self):
        """
        If trimmed length of the item description is a multiple of 3, 
        multiply the price by 0.2 and round up to the nearest integer. 
        The result is the number of points earned.
        """

        points = 0
        for item in self.items:
            trimmed_length = len(item.shortDescription.strip())
            if trimmed_length % 3 == 0:
                points += round(item.price * 0.2)
        return points
    
    def is_day_of_purchase_odd(self):
        return self.purchaseDate.day % 2 == 1
    
    def is_time_between_range(
        self, start_time: time = time(14, 0), end_time: time = time(16, 0)
    ):
        """ Check if the purchase time is between a range """
        return start_time <= self.purchaseTime <= end_time