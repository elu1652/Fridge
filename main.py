import sqlite3
from fridge import Fridge
from ingredient import Ingredient

f = Fridge()
i = Ingredient('Milk', 2, 'litres', '2021-12-31')
f.add_ingredient(i)
print(f.db)

