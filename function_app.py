import azure.functions as func
import json
from azure.cosmos import CosmosClient
import os

app = func.FunctionApp()

client = CosmosClient(os.getenv("COSMOS_URI"), credential=os.getenv("COSMOS_KEY"))
db = client.get_database_client("productsDB")
container = db.get_container_client("products")

@app.function_name(name="get_product")
@app.route(route="product/{prod_id}", methods=["GET"])
def get_product(req: func.HttpRequest) -> func.HttpResponse:
    prod_id = req.route_params.get("prod_id")
    item = container.read_item(prod_id, partition_key=prod_id)
    return func.HttpResponse(json.dumps(item), status_code=200)


@app.function_name(name="list_products")
@app.route(route="products", methods=["GET"])
def list_products(req: func.HttpRequest) -> func.HttpResponse:
    items = list(container.read_all_items())
    return func.HttpResponse(json.dumps(items), status_code=200)


@app.function_name(name="create_product")
@app.route(route="product", methods=["POST"])
def create_product(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    container.create_item(body)
    return func.HttpResponse("Created", status_code=201)


@app.function_name(name="update_product")
@app.route(route="product/{prod_id}", methods=["PUT"])
def update_product(req: func.HttpRequest) -> func.HttpResponse:
    prod_id = req.route_params.get("prod_id")
    body = req.get_json()
    body["id"] = prod_id
    container.replace_item(prod_id, body)
    return func.HttpResponse("Updated", status_code=200)


@app.function_name(name="delete_product")
@app.route(route="product/{prod_id}", methods=["DELETE"])
def delete_product(req: func.HttpRequest) -> func.HttpResponse:
    prod_id = req.route_params.get("prod_id")
    container.delete_item(prod_id, partition_key=prod_id)
    return func.HttpResponse("Deleted", status_code=204)

