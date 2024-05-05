import json
import os
from fastapi import FastAPI, HTTPException


app = FastAPI()

json_file_path = "inventory_data.json"


def load_products():
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            return json.load(file)
    else:
        return []


products = load_products()


@app.get("/all_products")
async def get_all_products():
    return products


@app.get("/products/{product_name}")
async def get_product_by_name(product_name: str):
    for product in products:
        if product["name"] == product_name:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/products/{product_name}/{product_field}")
async def get_product_field_by_name(product_name: str, product_field: str):
    for product in products:
        if product["name"] == product_name:
            if product_field in product["details"]:
                return {product_field: product["details"][product_field]}
            else:
                raise HTTPException(status_code=404, detail=f"Field '{product_field}' not found for product '{product_name}'")
    raise HTTPException(status_code=404, detail="Product not found")