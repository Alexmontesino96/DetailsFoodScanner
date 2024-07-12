from fastapi import FastAPI
from routers.router_product_identifier import router_product_identifier

app = FastAPI()
app.include_router(router_product_identifier)