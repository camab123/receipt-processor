import math
from datetime import date, datetime, time

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
        description="The date the receipt was issued.", examples=["2021-01-01"]
    )
    purchaseTime: str = Field(
        description="The time the receipt was issued.",
        examples=["13:01"],
        pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$",
    )
    items: list[Item] = Field(
        description="A list of items purchased on the receipt.", min_length=1
    )
    total: str = Field(
        description="The total amount paid on the receipt.", pattern="^\\d+\\.\\d{2}$",
        examples=["6.49"],
    )

    def get_points(self) -> int:
        """Calculate the points for the given receipt"""
        points = 0
        # Count of alphanumeric characters in the retailer name
        points += Receipt.alphanumeric_count(self.retailer)
        # Check if the total is a round number
        points += 50 if float(self.total).is_integer() else 0
        # Check if the total is a multiple of 0.25
        points += 25 if self.is_total_multiple_of_quarter() else 0
        # Add points for every 2 items purchased
        points += len(self.items) // 2 * 5
        # Add points if trimmed
        points += self.get_trimmed_description_value()
        # Add points if the day of purchase is odd
        points += 6 if self.is_day_of_purchase_odd() else 0
        # Add points if the purchase time is between 2pm and 4pm
        points += 10 if self.is_time_between_range() else 0

        return points

    @staticmethod
    def alphanumeric_count(value: str) -> int:
        return sum(char.isalnum() for char in value)

    def is_total_multiple_of_quarter(self):
        """Check if the total is a multiple of 0.25"""
        return float(self.total) % 0.25 == 0

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
                item_points = math.ceil(item.price * 0.2)
                points += item_points
        return points

    def is_day_of_purchase_odd(self):
        return self.purchaseDate.day % 2 == 1

    def is_time_between_range(
        self, start_time: time = time(14, 0), end_time: time = time(16, 0)
    ):
        """Check if the purchase time is between a range"""
        time_to_check = datetime.strptime(self.purchaseTime, "%H:%M").time()
        return start_time < time_to_check < end_time
