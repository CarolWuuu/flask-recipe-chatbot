import pandas as pd
import os
import kagglehub


def run_etl(output_path='data/healthy_recipes_clean.csv'):
    try:
        print("Downloading dataset from KaggleHub...")
        version_path = kagglehub.dataset_download("utsavdey1410/food-nutrition-dataset")

        # Locate CSV file
        csv_file = None
        for root, _, files in os.walk(version_path):
            for file in files:
                if file.lower().endswith(".csv"):
                    csv_file = os.path.join(root, file)
                    break
            if csv_file:
                break

        if not csv_file:
            raise FileNotFoundError("No CSV file found in the dataset folder.")

        print(f"📖 Reading CSV: {csv_file}")
        df = pd.read_csv(csv_file)

        # Drop index columns if they exist
        df.drop(columns=[col for col in ['Unnamed: 0', 'Unnamed: 0.1'] if col in df.columns], inplace=True)

        # Rename columns
        df.rename(columns={
            'food': 'name',
            'Caloric Value': 'calories_kcal',
            'Fat': 'fat_g',
            'Saturated Fats': 'saturated_fats_g',
            'Monounsaturated Fats': 'monounsaturated_fats_g',
            'Polyunsaturated Fats': 'polyunsaturated_fats_g',
            'Carbohydrates': 'carbohydrates_g',
            'Sugars': 'sugars_g',
            'Protein': 'protein_g',
            'Dietary Fiber': 'fiber_g',
            'Cholesterol': 'cholesterol_mg',
            'Sodium': 'sodium_mg',
            'Water': 'water_g',
            'Vitamin A': 'vitamin_a_mg',
            'Vitamin B1': 'vitamin_b1_thiamine_mg',
            'Vitamin B11': 'vitamin_b11_folic_acid_mg',
            'Vitamin B12': 'vitamin_b12_mg',
            'Vitamin B2': 'vitamin_b2_riboflavin_mg',
            'Vitamin B3': 'vitamin_b3_niacin_mg',
            'Vitamin B5': 'vitamin_b5_pantothenic_acid_mg',
            'Vitamin B6': 'vitamin_b6_mg',
            'Vitamin C': 'vitamin_c_mg',
            'Vitamin D': 'vitamin_d_mg',
            'Vitamin E': 'vitamin_e_mg',
            'Vitamin K': 'vitamin_k_mg',
            'Calcium': 'calcium_mg',
            'Copper': 'copper_mg',
            'Iron': 'iron_mg',
            'Magnesium': 'magnesium_mg',
            'Manganese': 'manganese_mg',
            'Phosphorus': 'phosphorus_mg',
            'Potassium': 'potassium_mg',
            'Selenium': 'selenium_mg',
            'Zinc': 'zinc_mg',
            'Nutrition Density': 'nutrition_density'
        }, inplace=True)

        # Drop any remaining exact duplicates
        df.drop_duplicates(inplace=True)

        # Save cleaned CSV
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)

        print(f"✅ ETL complete. Cleaned file saved to: {output_path}")

    except Exception as e:
        print(f"[ERROR] ETL failed: {e}")

if __name__ == "__main__":
        run_etl()