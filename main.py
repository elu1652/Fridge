import sqlite3
from fridge import Fridge
from ingredient import Ingredient
from recipe import Recipe,RecipeDB

f = Fridge()
i = Ingredient('Milk', 2, 'litres', '2021-12-31')
i2 = Ingredient('Milk', 0.5, 'units', '2021-12-31')
r = Recipe('Pancakes', [i2])

rdb = RecipeDB()
#rdb.add_recipe(r)
f.db.clear_table('ingredients')


print(f.db)

