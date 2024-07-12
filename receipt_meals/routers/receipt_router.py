from fastapi.routing import APIRouter


receipt_router = APIRouter()


@receipt_router.get('/receipts')
async def get_receipts():
    return {'message': 'Hello from receipts'}