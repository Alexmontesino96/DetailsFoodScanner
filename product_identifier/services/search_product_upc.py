import requests
import json
from fastapi.responses import JSONResponse
from product_schema.product import ProductSpoonacular
from product_schema.product import ProductOpenFoodFacts
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
import os
import dotenv


dotenv.load_dotenv('config.env')
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')

async def search_product_upc(upc):
    """
    Searches for a product using the given UPC code.

    Args:
        upc (str): The UPC code of the product.

    Returns:
        JSONResponse: The response containing the product information if found, or an error message if not found.

    Raises:
        HTTPException: If a server error occurs during the request.

    """
    services_name = str
    product = None

    # Request to OpenFoodFacts API or Spoonacular API
    try: 
        """
        Pending task: Implement function to complete the data with the other service
        """
        # url_openfood = 'https://us.openfoodfacts.org/api/v0/product/{upc}'

        url_spoonacular = 'https://api.spoonacular.com/food/products/upc/{upc}?apiKey={SPOONACULAR_API_KEY}'
        services_name = 'spoonacular'
        response = requests.get(url_spoonacular.format(upc=upc, SPOONACULAR_API_KEY=SPOONACULAR_API_KEY))

    except Exception as e:
        print('An ocurred error in the request to Spoonacular API:', e)
        return JSONResponse(content={'message': 'An ocurred error in the request to Spoonacular API'}, status_code=500)
    
    try:

        if response.status_code == 200 and response.json().get('status') != 'failure':

            if services_name == "openfood":
                #Initialize ProductOpenFoodFacts object with all attributes as 'N/A'
                product_open_food = ProductOpenFoodFacts()
                product_open_food.from_api_response(json.loads(response.text))
                return JSONResponse(content=jsonable_encoder(product_open_food), status_code=200)
            
            elif services_name == "spoonacular":
                product_spoonacular = ProductSpoonacular(**json.loads(response.text))
                return JSONResponse(content=jsonable_encoder(product_spoonacular), status_code=200)
        else:
            return JSONResponse(content={'message': 'Product not found'}, status_code=404)
        
    except Exception as e:
        print("An error occurred:", e)
        return HTTPException(content={'message': 'Server error'}, status_code=500)
    

def complete_none_data_with_diferent_service(product):
    pass
    #url_openfood = 'https://us.openfoodfacts.org/api/v0/product/{upc}'
    #url_spoonacular = 'https://api.spoonacular.com/food/products