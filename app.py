from flask import Flask, request, jsonify
import pandas as pd
from spoonacular_api.api_client import search_recipes
from flask import render_template


app = Flask(__name__)

# Load local dataset
try:
    df = pd.read_csv("data/healthy_recipes_clean.csv")
except Exception as e:
    print(f"[ERROR] Failed to load local data: {e}")
    df = pd.DataFrame()

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").lower()

    if not user_input:
        return jsonify({"response": "Please provide a message."})

    # Try matching with local dataset
    matches = df[df["name"].str.lower().str.contains(user_input)]

    if not matches.empty:
        top_match = matches.iloc[0]
        response = (
            f"Here's a recipe I found locally:\n"
            f"🍽️ {top_match['name']}\n"
            f"🔥 Calories: {top_match['calories_kcal']} kcal\n"
            f"💪 Protein: {top_match['protein_g']} g\n"
            f"🥑 Fat: {top_match['fat_g']} g\n"
            f"🍞 Carbs: {top_match['carbohydrates_g']} g"
        )
        return jsonify({"response": response})

    # If not found locally, call Spoonacular API
    api_results = search_recipes(query=user_input, number=1)
    if api_results:
        recipe = api_results[0]
        response = (
            f"Here's a recipe from Spoonacular:\n"
            f"🍽️ {recipe['title']}\n"
            f"🔗 Link: https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']}\n"
            f"🔥 Calories: {recipe['nutrition']['nutrients'][0]['amount']} kcal"
        )
    else:
        response = "Sorry, I couldn't find a matching recipe."

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
