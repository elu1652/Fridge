import sqlite3
from database import Database
from ingredient import Ingredient
from recipe import Recipe

class Fridge:
    def __init__(self):
        self.db = Database()
    
    def add_ingredient(self,ingredient):
        self.db.add_item(ingredient)

    def cook(self,recipe):
        for i in recipe.ingredients:
            self.db.delete_item(i)
    
    def add_recipe(self,recipe):
        self.db.add_recipe(recipe)

    def delete_recipe(self,recipe):
        self.db.delete_recipe(recipe)