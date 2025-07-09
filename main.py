# main.py
# No changes to how you run this file: uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Pydantic Models (Data Schemas) ---
class Chef(BaseModel):
    name: str
    avatarUrl: str = Field(..., alias="avatarUrl")
    publishedDate: str = Field(..., alias="publishedDate")
class Meta(BaseModel):
    prepTime: int = Field(..., alias="prepTime")
    cookTime: int = Field(..., alias="cookTime")
    servings: int
class IngredientItem(BaseModel):
    id: str
    name: str
    quantity: float
    unit: str
    notes: Optional[str] = None
class IngredientGroup(BaseModel):
    group: str
    items: List[IngredientItem]
class Insight(BaseModel):
    id: str
    title: str
    content: str
class Recipe(BaseModel):
    id: int
    title: str
    category: str
    description: str
    chef: Chef
    meta: Meta
    imageUrl: str = Field(..., alias="imageUrl")
    ingredients: List[IngredientGroup]
    instructions: List[str]
    insights: List[Insight]
class RecipeTeaser(BaseModel):
    id: int
    title: str
    category: str
    imageUrl: str = Field(..., alias="imageUrl")
    cookTime: int = Field(..., alias="cookTime")

# --- Mock Database ---
DB_RECIPES = {
    1: {
        "id": 1,
        "title": "The Ultimate Avocado Egg Cheese Toast",
        "category": "Breakfast",
        "description": "A breakfast masterpiece that perfectly balances creamy avocado, savory omelette, and melted cheese on crisp, buttery sourdough. It's a hearty, satisfying meal to kickstart your day.",
        "chef": {"name": "Your Kitchen", "avatarUrl": "https://placehold.co/100x100/E2E8F0/4A5568?text=YK", "publishedDate": "July 8, 2025"},
        "meta": {"prepTime": 10, "cookTime": 10, "servings": 1},
        "imageUrl": "https://images.unsplash.com/photo-1525351484163-7529414344d8?q=80&w=2080&auto=format&fit=crop",
        "ingredients": [
            {
                "group": "For the Toast",
                "items": [
                    {"id": 'ing1', "name": "Sourdough Bread", "quantity": 2, "unit": "thick slices", "notes": "or gluten-free bread"},
                    {"id": 'ing2', "name": "Unsalted Butter", "quantity": 1, "unit": "tbsp", "notes": "or lactose-free spread"},
                    {"id": 'ing3', "name": "Hard Cheese (e.g., Cheddar)", "quantity": 2, "unit": "slices", "notes": "naturally low in lactose"},
                ],
            },
            {
                "group": "For the Avocado & Egg",
                "items": [
                    {"id": 'ing4', "name": "Large Egg", "quantity": 1, "unit": ""},
                    {"id": 'ing5', "name": "Lactose-Free Milk", "quantity": 1, "unit": "tbsp", "notes": "optional"},
                    {"id": 'ing6', "name": "Avocado", "quantity": 0.25, "unit": "medium", "notes": "1/8 per serving is low-FODMAP"},
                    {"id": 'ing7', "name": "Salt", "quantity": 1, "unit": "pinch", "notes": "to taste"},
                    {"id": 'ing8', "name": "Black Pepper", "quantity": 1, "unit": "pinch", "notes": "to taste"},
                ],
            },
        ],
        "instructions": ["Toast your bread...", "Make the omelette...", "Mash a small amount of avocado...", "Assemble and enjoy."],
        "insights": [{"id": 'ins1', "title": "FODMAP Note on Avocado", "content": "Avocado is a healthy fat, but it's high in FODMAPs in large servings. A serving of 1/8th of an avocado is generally considered safe for most people on a low-FODMAP diet."}],
    },
    2: {
        "id": 2,
        "title": "Gentle Tomato & Basil Pasta",
        "category": "Gut-Friendly Dinner",
        "description": "A classic Italian dish remade to be gentle on your system. All the flavor, none of the common triggers.",
        "chef": {"name": "The Gentle Chef", "avatarUrl": "https://placehold.co/100x100/A7F3D0/047857?text=GC", "publishedDate": "July 1, 2025"},
        "meta": {"prepTime": 5, "cookTime": 20, "servings": 2},
        "imageUrl": "https://images.unsplash.com/photo-1574484284002-952d92456975?q=80&w=1974&auto=format&fit=crop",
        "ingredients": [
            {
                "group": "Main",
                "items": [
                    {"id": 'ing9', "name": "Gluten-Free Spaghetti", "quantity": 200, "unit": "g", "notes": "rice or corn-based"},
                    {"id": 'ing19', "name": "Canned Chopped Tomatoes", "quantity": 400, "unit": "g", "notes": "check for no added onion/garlic"},
                    {"id": 'ing20', "name": "Garlic-Infused Olive Oil", "quantity": 2, "unit": "tbsp"},
                    {"id": 'ing21', "name": "Fresh Basil", "quantity": 1, "unit": "handful"},
                ],
            }
        ],
        "instructions": [
            "Cook gluten-free pasta according to package directions.",
            "While pasta cooks, gently heat the garlic-infused oil in a pan.",
            "Add the canned tomatoes, season with salt and pepper, and simmer for 10 minutes.",
            "Toss the cooked pasta with the sauce and fresh basil. Serve immediately.",
        ],
        "insights": [{"id": 'ins3', "title": "Why Garlic-Infused Oil?", "content": "FODMAPs in garlic are water-soluble, not oil-soluble. This means the oil gets the beautiful garlic flavor without any of the fructans that can cause digestive issues."}],
    },
    3: {
        "id": 3,
        "title": "Shrimp Scampi with Gentle Garlic-Infused Oil",
        "category": "Gut-Friendly Dinner",
        "description": "A sophisticated and flavorful pasta dish that's surprisingly easy on the digestive system. A true crowd-pleaser.",
        "chef": {"name": "The Gentle Chef", "avatarUrl": "https://placehold.co/100x100/A7F3D0/047857?text=GC", "publishedDate": "July 15, 2025"},
        "meta": {"prepTime": 10, "cookTime": 15, "servings": 2},
        "imageUrl": "https://images.unsplash.com/photo-1599599810694-b5b37304c047?q=80&w=1965&auto=format&fit=crop",
        "ingredients": [
            {
                "group": "Main",
                "items": [
                    {"id": 'ing10', "name": "Gluten-Free Linguine", "quantity": 200, "unit": "g"},
                    {"id": 'ing12', "name": "Large Shrimp", "quantity": 250, "unit": "g", "notes": "peeled and deveined"},
                ],
            },
            {
                "group": "For the Sauce",
                "items": [
                    {"id": 'ing13', "name": "Butter", "quantity": 2, "unit": "tbsp", "notes": "or lactose-free alternative"},
                    {"id": 'ing20', "name": "Garlic-Infused Olive Oil", "quantity": 2, "unit": "tbsp"},
                    {"id": 'ing16', "name": "Lemon Juice", "quantity": 1, "unit": "tbsp"},
                    {"id": 'ing17', "name": "Fresh Parsley", "quantity": 2, "unit": "tbsp", "notes": "chopped"},
                ],
            },
        ],
        "instructions": [
            "Cook gluten-free pasta according to package directions. Reserve 1/2 cup of pasta water.",
            "In a large skillet, melt butter and garlic-infused oil over medium heat.",
            "Add shrimp and cook for 1-2 minutes per side until pink. Remove shrimp from pan.",
            "Add lemon juice to the pan, then return shrimp and add cooked pasta and parsley.",
            "Toss everything to combine, adding a splash of pasta water to create a silky sauce. Serve immediately.",
        ],
        "insights": [{"id": 'ins4', "title": "Don't Overcook the Shrimp", "content": "Shrimp cook very quickly. They're done as soon as they turn pink and curl into a 'C' shape. An overcooked shrimp will be tough and rubbery."}],
    },
}

# --- FastAPI Application ---
app = FastAPI(title="Recipe API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)
@app.get("/")
def read_root(): return {"message": "Welcome to the Gut-Friendly Recipe API!"}
@app.get("/api/recipes", response_model=List[RecipeTeaser])
def get_all_recipes():
    teasers = []
    for recipe_id, recipe in DB_RECIPES.items(): teasers.append({ "id": recipe["id"], "title": recipe["title"], "category": recipe["category"], "imageUrl": recipe["imageUrl"], "cookTime": recipe["meta"]["cookTime"] })
    return teasers
@app.get("/api/recipes/{recipe_id}", response_model=Recipe)
def get_recipe_by_id(recipe_id: int):
    recipe = DB_RECIPES.get(recipe_id)
    if not recipe: raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
