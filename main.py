from fastapi import FastAPI, Query
from typing import Annotated
from enum import Enum
from pydantic import BaseModel

class Item(BaseModel):
 name: str
 description: str | None = None
 price: float
 tax: float | None = None

app = FastAPI()

@app.get("/")
async def root():
  return { "message": "Hello World" }


# fake_items_db = [{ "item_name": "Foo" }, { "item_name": "Bar" }, {"item_name": "Baz"}]

# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#   return fake_items_db[skip : skip + limit];

# @app.get("/items/{item_id}")
# async def read_user_item(item_id: str, needy: str):
#   item = { "item_id": item_id, "needy": needy }
#   return item

@app.post("/items/")
async def create_item(item: Item):
  item_dict = item.model_dump()

  if item.tax:
    price_with_tax = item.price + item.tax
    item_dict.update({ "price_with_tax": price_with_tax })


  return item_dict

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
  result = { "item_id": item_id, **item.model_dump() }
  if q:
    result.update({ "q": q })
  return result

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
  results = { "items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
  if q:
     results.update({"q" : q})
  return results

@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: int | None = None):
  item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
  return item

@app.get("/users/me")
async def read_user_me():
  return { "user_id": "the current user" }

@app.get("/users/{user_id}")
async def read_user(user_id: str):
  return { "user_id": user_id }

### Predefined value
class ModelName(str, Enum):
  alexnet = "alexnet"
  resnet = "resnet"
  lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
  print("model_name >>> ", model_name.value)
  if model_name is ModelName.alexnet:
    return { "model_name": model_name, "message": "Deep Learning FTW!" }
  if model_name.value == "lenet":
    return { "model_name": model_name, "message": "LeCNN all the images"}
  return { "model_name": model_name, "message": "Have some residuals" }

@app.get("/files/{file_path: path}")
async def read_file(file_path: str):
  return { "file_path": file_path }

