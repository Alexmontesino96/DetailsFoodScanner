from fastapi.routing import APIRouter
from fastapi import HTTPException
from services.search_product_upc import search_product_upc
from product_schema.product import ProductOpenFoodFacts,ProductSpoonacular
from typing import Annotated, Union
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.search_product_by_name import ProductSearchParams, search_product_by_name_services
from fastapi.params import Path, Query

router_product_identifier = APIRouter()


@router_product_identifier.get("/product-identifier/upc/{upc}")
async def get_product_by_upc(upc: str):

    return await search_product_upc(upc)

    

@router_product_identifier.get("/product-identifier/search")
def search_product_by_name(
    query: str = Query(..., min_length=1, title="Product Name", description="The name of the product to search for"), 
    offset: int = Query(0, title="Offset", description="The number of products to skip"), 
    number: int = Query(10, title="Number", description="The number of products to return")):
    """
    Search for a product by its name.

    Args:
        query (str): The name of the product to search for.
        offset (int): The number of products to skip.
        number (int): The number of products to return.

    Returns:
        The search results for the specified product name.
    """
    parameters = ProductSearchParams(query=query, offset=offset, number=number)
    
    return search_product_by_name_services(parameters)