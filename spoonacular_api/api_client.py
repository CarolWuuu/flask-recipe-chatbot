import requests

API_KEY = "0261820092934a378cd8c1609e80740e"
BASE_URL = "https://api.spoonacular.com"

def search_recipes(query=None, diet=None, max_calories=None, number=3):
    """
    Search for recipes using optional filters.
    """
    endpoint = f"{BASE_URL}/recipes/complexSearch"
    params = {
        "apiKey": API_KEY,
        "number": number,
        "addRecipeNutrition": True
    }

    if query:
        params["query"] = query
    if diet:
        params["diet"] = diet
    if max_calories:
        params["maxCalories"] = max_calories

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        print(f"[ERROR] Spoonacular API search failed: {e}")
        return []

def get_recipe_info(recipe_id):
    """
    Get detailed info for a recipe by ID.
    """
    endpoint = f"{BASE_URL}/recipes/{recipe_id}/information"
    params = {
        "apiKey": API_KEY,
        "includeNutrition": True
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to get recipe info: {e}")
        return None
