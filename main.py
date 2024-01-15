import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

app = FastAPI()



def custom_openapi():

    if app.openapi_schema:

        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Example Web API",
        version="0.0.1",
        description="FastAPIで作ったWebAPIです。",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema

    return app.openapi_schema

app.openapi = custom_openapi

class Item(BaseModel):
    name: str
    price: int

@app.get(

    "/items/{item_name}",
    summary="アイテム取得",
    description="指定されたアイテムを取得し返却します。",
)

def get_item(item_name):
    return {"name": item_name, "price": 200}

@app.post(

    "/items/new",
    summary="アイテム追加",
    description="渡されたアイテムを追加します。",
)

def add_item(item: Item):
    return item

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

