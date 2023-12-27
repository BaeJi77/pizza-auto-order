from typing import List, Optional

from pydantic import BaseModel


class PizzaOrder(BaseModel):
    customer_name: str
    pizza_type: str
    size: str
    toppings: Optional[List[str]] = None
    address: str
    phone_number: str
