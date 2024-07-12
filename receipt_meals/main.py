from fastapi import FastAPI
from routers.receipt_router import receipt_router


app = FastAPI()
app.include_router(receipt_router)