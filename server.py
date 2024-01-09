from fastapi import FastAPI

from dto import OrderDTO

app = FastAPI()


@app.post("/order")
async def create_order(order: OrderDTO):
    print(order)

    return order
