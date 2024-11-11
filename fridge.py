import sqlite3
from database import Database

class fridge:
    def __init__(self):
        self.db = Database()
    
    def add_ingredient(self,name,quantity,unit,expiry_date):
        self.db.add_item(name,quantity,unit,expiry_date)