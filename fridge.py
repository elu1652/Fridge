import sqlite3
from database import Database
from ingredient import Ingredient

class Fridge:
    def __init__(self):
        self.db = Database()
    
    def add_ingredient(self,ingredient):
        self.db.add_item(ingredient)