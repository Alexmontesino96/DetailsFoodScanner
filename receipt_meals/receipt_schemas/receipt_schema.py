from typing_extensions import Unpack
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional, Dict
import requests
from product_identifier.product_schema.product import Nutrition, Nutrient

response = requests.get(f'https://api.spoonacular.com/recipes/716429/information?includeNutrition=false&apiKey=0f03d338669640b6b1e5453a39a1a621')
receipt = response.json()
print(receipt.keys())

class Measures(BaseModel):
    amount: float
    unitShort: str
    unitLong: str

class ExtendedIngredient(BaseModel):
    id: int
    aisle: str
    image: str
    consistency: str
    name: str
    nameClean: str
    original: str
    originalName: str
    amount: float
    unit: str
    meta: List[str]
    measures: Dict[str, Measures]

class Recipe(BaseModel):
    vegetarian: bool
    vegan: bool
    glutenFree: bool
    dairyFree: bool
    veryHealthy: bool
    cheap: bool
    veryPopular: bool
    sustainable: bool
    lowFodmap: bool
    weightWatcherSmartPoints: int
    gaps: str
    preparationMinutes: Optional[int]
    cookingMinutes: Optional[int]
    aggregateLikes: int
    healthScore: int
    creditsText: str
    license: str
    sourceName: str
    pricePerServing: float
    extendedIngredients: List[ExtendedIngredient]
    id: int
    title: str
    readyInMinutes: int
    servings: int
    sourceUrl: str
    image: str
    imageType: str
    nutrition: Nutrition
    summary: str
    cuisines: List[str]
    dishTypes: List[str]
    diets: List[str]
    occasions: List[str]
    instructions: str
    analyzedInstructions: List[str]
    originalId: Optional[int]
    spoonacularScore: float
    spoonacularSourceUrl: str




