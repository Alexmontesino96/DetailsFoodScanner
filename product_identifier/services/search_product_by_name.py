from pydantic import BaseModel
from typing import Optional
import requests
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json
from fastapi.exceptions import HTTPException
import os
import dotenv


dotenv.load_dotenv('config.env')
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')



class ProductSearchParams(BaseModel):
    query: str
    offset: Optional[int] = 0
    number: Optional[int] = 10


def search_product_by_name_services(params: ProductSearchParams):
    """
    Search for a product by name using the Spoonacular API.

    Args:
        params (ProductSearchParams): An object containing the search parameters.

    Returns:
        JSONResponse: The response containing the search results.

    Raises:
        JSONResponse: If the product is not found.
        HTTPException: If there is a server error.
    """
    
    url_spoonacular = 'https://api.spoonacular.com/food/search?query={params.query}&offset={params.offset}&number={params.number}&apiKey={SPOONACULAR_API_KEY}'
    services_name = 'spoonacular'

    response = requests.get(url_spoonacular.format(params=params, API_KEY=SPOONACULAR_API_KEY))

    result = response.json()

    if response.status_code == 200 and response.json().get('status') != 'failure':
        return JSONResponse(content=result, status_code=200)
    
    elif response.status_code == 404:
        return JSONResponse(content={'message': 'Product not found'}, status_code=404)
    
    elif response.status_code == 500:
        return HTTPException(content={'message': 'Server error'}, status_code=500)
