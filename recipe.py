from ingredient import Ingredient
import sqlite3
class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = []
        for i in ingredients:
            self.ingredients.append(i)
