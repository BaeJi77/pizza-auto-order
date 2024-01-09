from typing import List, Optional

from pydantic import BaseModel, conint


class PizzaOrder(BaseModel):
    type: str
    size: str


class SideOrder(BaseModel):
    item: str
    size: Optional[str] = None


class ToppingOrder(BaseModel):
    topping: str


class BeverageOrder(BaseModel):
    beverage: str
    size: Optional[str] = None


class OrderDTO(BaseModel):
    pizzas: List[PizzaOrder]
    sides: Optional[List[SideOrder]] = None
    toppings: Optional[List[ToppingOrder]] = None
    beverages: Optional[List[BeverageOrder]] = None
    total_price: conint(ge=0)  # Ensure the total price is greater than or equal to 0
