from ingredient import Ingredient
import sqlite3
class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = []
        for i in ingredients:
            self.ingredients.append(i)

class RecipeDB:
    def __init__(self, db_name='fridge.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._create_table()

    def _create_table(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL
                            )''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS ingredients (
                                id INTEGER PRIMARY KEY,
                                recipe_id INTEGER,
                                ingredient_name TEXT NOT NULL,
                                quantity REAL NOT NULL,
                                unit TEXT NOT NULL,
                                FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
                            )''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table {e}")
    
    def add_recipe(self,recipe):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''INSERT INTO recipes (name) VALUES (?)''',(recipe.name,))
            recipe_id = self.cursor.lastrowid
            for i in recipe.ingredients:
                self.cursor.execute('''INSERT INTO ingredients (recipe_id,ingredient_name,quantity,unit) VALUES (?,?,?,?)''',(recipe_id,i.name,i.quantity,i.unit))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding recipe {e}")
