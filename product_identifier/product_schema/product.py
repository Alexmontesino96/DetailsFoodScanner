from pydantic import BaseModel, Field, field_validator
from typing import List, Optional



class Nutrient(BaseModel):
    name: Optional[str]
    amount: Optional[float]
    unit: Optional[str]
    percentOfDailyNeeds: Optional[float]



class Nutrition(BaseModel):
    
    nutrients: List[Nutrient]
    caloricBreakdown: dict
    calories: Optional[float] = Field(None, alias='calories')
    fat: Optional[float] = Field(None, alias='fat')
    protein: Optional[float]= Field(None, alias='protein')
    carbs: Optional[float] = Field(None, alias='carbs')

    @field_validator('nutrients', mode='before')
    def check_type(cls, value):
        nutrient_list = []
        for nutrient in value:
            try:
                nutrient_list.append(Nutrient(**nutrient))
            except:
                 continue
        return nutrient_list
                

    @field_validator('fat', 'protein','carbs', mode='before')
    def parse_amount(cls, value):
        if isinstance(value, str or None):
            try:
                # Intenta convertir la cadena a un número
                return float(value.replace('g', '').replace('mg', '').replace('µg', '').replace('cal', '').strip())
            except ValueError:
                raise ValueError(f"Invalid value for amount: {value}")
        else:
            return value
          



class Servings(BaseModel):
    number: Optional[int]
    size: Optional[float]
    unit: Optional[str]
    raw: Optional[str]

    @field_validator('number', mode='before')
    def parse_number(cls, value):
        if isinstance(value, float):
             return round(value)

class Credits(BaseModel):
        text: str
        link: str
        image: str
        imageLink: str

class ProductSpoonacular(BaseModel):
        id: int
        title: str
        badges: List[str]
        importantBadges: List[str]
        breadcrumbs: List[str]
        category: str
        usdaCode: Optional[str]
        price: float
        likes: int
        nutrition: Nutrition
        servings: Servings
        spoonacularScore: Optional[float]
        aisle: Optional[str]
        description: Optional[str]
        image: str
        imageType: str
        images: List[str]
        generatedText: Optional[str]
        upc: str
        brand: Optional[str]
        ingredients: List[dict]
        ingredientCount: int
        ingredientList: str
        credits: Credits

        def __str__(self):
            ingredients_str = "\n".join([str(ingredient) for ingredient in self.ingredients])
            return (f"ID: {self.id}\n"
                    f"Nombre del Producto: {self.title}\n"
                    f"Distintivos: {', '.join(self.badges)}\n"
                    f"Distintivos Importantes: {', '.join(self.importantBadges)}\n"
                    f"Categoría: {self.category}\n"
                    f"Código USDA: {self.usdaCode}\n"
                    f"Precio: {self.price}\n"
                    f"Likes: {self.likes}\n"
                    f"Nutrición: {(self.nutrition)}\n"
                    f"Porciones: {self.servings}\n"
                    f"Puntaje Spoonacular: {self.spoonacularScore}\n"
                    f"Pasillo: {self.aisle}\n"
                    f"Descripción: {self.description}\n"
                    f"Imagen: {self.image}\n"
                    f"Tipo de Imagen: {self.imageType}\n"
                    f"Imágenes: {', '.join(self.images)}\n"
                    f"Texto Generado: {self.generatedText}\n"
                    f"UPC: {self.upc}\n"
                    f"Marca: {self.brand}\n"
                    f"Ingredientes: {ingredients_str}\n"
                    f"Cantidad de Ingredientes: {self.ingredientCount}\n"
                    f"Lista de Ingredientes: {self.ingredientList}\n"
                    f"Créditos: {self.credits}")

class ProductOpenFoodFacts(BaseModel):
        product_name: str = 'N/A'
        brand_owner: str = 'N/A'
        code: str = 'N/A'
        countries: str = 'N/A'
        created_t: str = 'N/A'
        last_modified_t: str = 'N/A'
        calories: str = 'N/A'
        fat: str = 'N/A'
        saturated_fat: str = 'N/A'
        carbohydrates: str = 'N/A'
        sugars: str = 'N/A'
        fiber: str = 'N/A'
        proteins: str = 'N/A'
        sodium: str = 'N/A'
        salt: str = 'N/A'
        calcium: str = 'N/A'
        iron: str = 'N/A'
        cholesterol: str = 'N/A'
        ingredients_text: str = 'N/A'
        additives: List[str] = []
        allergens: str = 'N/A'
        ecoscore_grade: str = 'N/A'
        ecoscore_data: dict = {}
        allergens_hierarchy: List[str] = []
        vegan_status: List[str] = []
        vegetarian_status: List[str] = []
        popularity_tags: List[str] = []
        nutriscore_grade: str = 'N/A'
        nova_group: str = 'N/A'
        image: str = 'N/A'

        @classmethod
        def from_api_response(cls, api_response):
            product = cls()
            product.product_name = api_response.get('product_name', 'N/A')
            product.brand_owner = api_response.get('brand_owner', 'N/A')
            product.code = api_response.get('code', 'N/A')
            product.countries = api_response.get('countries', 'N/A')
            product.created_t = api_response.get('created_t', 'N/A')
            product.last_modified_t = api_response.get('last_modified_t', 'N/A')
            
            nutriments = api_response.get('nutriments', {})
            product.calories = nutriments.get('energy-kcal_value', 'N/A')
            product.fat = nutriments.get('fat_value', 'N/A')
            product.saturated_fat = nutriments.get('saturated-fat_value', 'N/A')
            product.carbohydrates = nutriments.get('carbohydrates_value', 'N/A')
            product.sugars = nutriments.get('sugars_value', 'N/A')
            product.fiber = nutriments.get('fiber_value', 'N/A')
            product.proteins = nutriments.get('proteins_value', 'N/A')
            product.sodium = nutriments.get('sodium_value', 'N/A')
            product.salt = nutriments.get('salt_value', 'N/A')
            product.calcium = nutriments.get('calcium_value', 'N/A')
            product.iron = nutriments.get('iron_value', 'N/A')
            product.cholesterol = nutriments.get('cholesterol_value', 'N/A')
            
            product.ingredients_text = api_response.get('ingredients_text', 'N/A')
            product.additives = api_response.get('additives_tags', [])
            product.allergens = api_response.get('allergens', 'N/A')
            
            product.ecoscore_grade = api_response.get('ecoscore_grade', 'N/A')
            product.ecoscore_data = api_response.get('ecoscore_data', {})
            
            product.allergens_hierarchy = api_response.get('allergens_hierarchy', [])
            product.vegan_status = api_response.get('ingredients_analysis', {}).get('en:vegan-status-unknown', [])
            product.vegetarian_status = api_response.get('ingredients_analysis', {}).get('en:vegetarian-status-unknown', [])
            
            product.popularity_tags = api_response.get('popularity_tags', [])
            
            product.nutriscore_grade = api_response.get('nutriscore_grade', 'N/A')
            product.nova_group = api_response.get('nova_group', 'N/A')
            product.image = api_response.get('image_front_url', {})
            
            return product

        def __str__(self):
            return (f"Nombre del Producto: {self.product_name}\n"
                    f"Marca: {self.brand_owner}\n"
                    f"Código del Producto: {self.code}\n"
                    f"Países de Comercialización: {self.countries}\n"
                    f"Fecha de Creación: {self.created_t}\n"
                    f"Última Modificación: {self.last_modified_t}\n"
                    f"Calorías: {self.calories} kcal\n"
                    f"Grasas Totales: {self.fat} g\n"
                    f"Grasas Saturadas: {self.saturated_fat} g\n"
                    f"Carbohidratos Totales: {self.carbohydrates} g\n"
                    f"Azúcares: {self.sugars} g\n"
                    f"Fibra: {self.fiber} g\n"
                    f"Proteínas: {self.proteins} g\n"
                    f"Sodio: {self.sodium} mg\n"
                    f"Sal: {self.salt} mg\n"
                    f"Calcio: {self.calcium} mg\n"
                    f"Hierro: {self.iron} mg\n"
                    f"Colesterol: {self.cholesterol} mg\n"
                    f"Ingredientes: {self.ingredients_text}\n"
                    f"Aditivos: {', '.join(self.additives)}\n"
                    f"Alergenos: {self.allergens}\n"
                    f"Ecoscore: {self.ecoscore_grade}\n"
                    f"Nutriscore: {self.nutriscore_grade}\n"
                    f"Grupos Nova: {self.nova_group}\n"
                    f"Alergenos Jerarquía: {', '.join(self.allergens_hierarchy)}\n"
                    f"Estado Vegano: {', '.join(self.vegan_status)}\n"
                    f"Estado Vegetariano: {', '.join(self.vegetarian_status)}\n"
                    f"Popularidad: {', '.join(self.popularity_tags)}\n"
                    f"Imagen: {self.image}")
