import sqlite3
import pandas as pd
from config import PATH_XLSX, PATH_DB

df_recipes = pd.read_excel(PATH_XLSX, sheet_name='recipe')
df_food_category = pd.read_excel(PATH_XLSX, sheet_name='food_category')
df_meal_type = pd.read_excel(PATH_XLSX, sheet_name='meal_type')
df_ingredients = pd.read_excel(PATH_XLSX, sheet_name='ingredients')
df_recipe_ingredients = pd.read_excel(
    PATH_XLSX, sheet_name='recipe_ingredients',
    usecols=['recipe_id', 'ingredient_id', 'ingredient_qty', 'measurement_id']
)
print('Done readeing recipes.xlsx')

# Create SQLite database connection
conn = sqlite3.connect(PATH_DB)

# Write DataFrames to SQLite tables
df_recipes.to_sql('recipe', conn, index=False, if_exists='replace')
df_food_category.to_sql('food_category', conn, index=False, if_exists='replace')
df_meal_type.to_sql('meal_type', conn, index=False, if_exists='replace')
df_ingredients.to_sql('ingredients', conn, index=False, if_exists='replace')
df_recipe_ingredients.to_sql('recipe_ingredients', conn, index=False, if_exists='replace')

# Close database connection
conn.close()
print('Created recipes.db')