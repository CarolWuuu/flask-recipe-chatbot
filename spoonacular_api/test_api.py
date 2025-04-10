from spoonacular_api.api_client import search_recipes

results = search_recipes(query="salad", diet="vegan", max_calories=300)

for r in results:
    print(f"{r['title']} - {r['nutrition']['nutrients'][0]['amount']} kcal")