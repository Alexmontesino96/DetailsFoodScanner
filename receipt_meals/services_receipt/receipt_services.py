import requests
from dotenv import load_dotenv
import os
from receipt_schemas.receipt_schema import Recipe
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

load_dotenv('config.env')
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')


def get_receipts_by_id(receipt_id: int):
    try:
        response = requests.get(
            f'https://api.spoonacular.com/recipes/{receipt_id}/information?includeNutrition=true&apiKey={SPOONACULAR_API_KEY}')
        
        if response.status_code == 404:
            return JSONResponse(status_code=404, content={'Error': 'Receipt not found'})

        elif response.status_code == 200:
            new_receipt = Recipe(**response.json())
            return JSONResponse(status_code=200, content=jsonable_encoder(new_receipt))

        else:
            print({'Error': 'An error occurred'})
            return JSONResponse(status_code=500, content={'Error': response.json()})

    except Exception as e:
        print({'Error': 'An error occurred: ' + str(e)})
        return JSONResponse(status_code=500, content={'Error': 'An error occurred'})


def get_receipts_by_diet(diet: str):
    pass