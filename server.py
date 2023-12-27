from fastapi import FastAPI

from dto import PizzaOrder

app = FastAPI()


@app.post("/order")
async def create_order(order: PizzaOrder):
    print(order)

    return order
