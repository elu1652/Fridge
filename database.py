import sqlite3

class Database:
    def __init__(self,db_name='fridge.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._create_table()

    def _create_table(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS fridge (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                quantity INTEGER NOT NULL,
                                unit TEXT NOT NULL,
                                expiry_date TEXT NOT NULL
                            )''')
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

    def execute_query(self, query, params=None):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
    
    def add_item(self,name,quantity,unit,expiry_date):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''INSERT INTO fridge (name,quantity,unit,expiry_date) VALUES (?,?,?,?)''',(name,quantity,unit,expiry_date))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding item {e}")
    
    def add_item(self,ingredient):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''SELECT quantity FROM fridge WHERE name = ?''',(ingredient.name,))
            item = self.cursor.fetchone()
            if item:
                new_quantity = item[0] + ingredient.quantity
                self.cursor.execute('''UPDATE fridge SET quantity = ? WHERE name = ?''',(new_quantity,ingredient.name))
            else:
                self.cursor.execute('''INSERT INTO fridge (name,quantity,unit,expiry_date) VALUES (?,?,?,?)''',(ingredient.name,ingredient.quantity,ingredient.unit,ingredient.expiry_date))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding item {e}")

    def delete_item(self,ingredient):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''SELECT quantity FROM fridge WHERE name = ?''',(ingredient.name,))
            result = self.cursor.fetchone()

            if result:
                current_quantity = result[0]
                new_quantity = current_quantity - ingredient.quantity
                
                if new_quantity < 0:
                    print(f"Error: Not enough {ingredient.name} in fridge")
                    return
                elif new_quantity == 0:
                    self.cursor.execute('''DELETE FROM fridge WHERE name = ?''',(ingredient.name,))
                else:
                    self.cursor.execute('''UPDATE fridge SET quantity = ? WHERE name = ?''',(new_quantity,ingredient.name))
                self.conn.commit()
            else:
                print(f"Error: {ingredient.name} not found in fridge")
        except sqlite3.Error as e:
            print(f"Error deleting item {e}")

    #Delete recipe
        


    def close(self):
        if self.conn:
            self.conn.close()

    def __str__(self):
        try:
            self.cursor.execute('''SELECT * FROM fridge''')
            rows = self.cursor.fetchall()
            output = "Fridge contents:\n"
            if rows:
                output += '\n'.join([f"ID: {row[0]}, Name: {row[1]}, Quantity: {row[2]}, Unit: {row[3]}, Expiry: {row[4]}" for row in rows])
            else:
                output += "\nNo items in fridge\n"

            output += "\n\nRecipes:\n"
            
            self.cursor.execute('''SELECT * FROM recipes''')
            rows = self.cursor.fetchall()
            if rows:
                output += '\n'.join([f"ID: {row[0]}, Name: {row[1]}" for row in rows])
            else:
                output += "\nNo recipes in database\n"
            
            output += "\n\nIngredients:\n"        

            self.cursor.execute('''SELECT * FROM ingredients''')
            rows = self.cursor.fetchall()
            if rows:
                output += '\n'.join([f"ID: {row[0]}, Recipe ID: {row[1]}, Name: {row[2]}, Quantity: {row[3]}, Unit: {row[4]}" for row in rows])
            else:
                output += "\nNo ingredients in database\n"
            return output

        except sqlite3.Error as e: 
            print(f"Error fetching data {e}")
            return "Error fetching data"
    
    def clear_table(self,table):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f'''DELETE FROM {table}''')
            if table == "recipes":
                self.cursor.execute('''DELETE FROM ingredients''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error clearing table {e}")

    def delete_recipe(self,recipe):
        try:
            self.cursor.execute('''SELECT id FROM recipes WHERE name = ?''',(recipe.name,))
            result = self.cursor.fetchone()
            recipe_id = result[0]
            self.cursor.execute('''DELETE FROM recipes WHERE name = ?''',(recipe.name,))
            self.cursor.execute('''DELETE FROM ingredients WHERE recipe_id = ?''',(recipe_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting recipe {e}")
