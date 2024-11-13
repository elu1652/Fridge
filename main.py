import sqlite3
from fridge import Fridge
from ingredient import Ingredient
from recipe import Recipe

f = Fridge()
i = Ingredient('Milk', 2, 'litres', '2021-12-31')
i2 = Ingredient('Milk', 0.5, 'units', '2021-12-31')
i3 = Ingredient('Eggs', 3, 'units', '2021-12-31')
i4 = Ingredient('Eggs', 6, 'units', '2021-12-31')
i5 = Ingredient('Flour', 500, 'grams', '2021-12-31')
i6 = Ingredient('Flour', 200, 'grams', '2021-12-31')
r = Recipe('Pancakes', [i2])
r2 = Recipe('Cake', [i3,i6])

f.cook(r2)

print(f.db)

