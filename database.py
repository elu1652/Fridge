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
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table {e}")


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

            output += "\nRecipes:\n"
            
            self.cursor.execute('''SELECT * FROM recipes''')
            rows = self.cursor.fetchall()
            if rows:
                output += '\n'.join([f"ID: {row[0]}, Name: {row[1]}" for row in rows])
            else:
                output += "\nNo recipes in database\n"
            
            output += "\nIngredients:\n"        

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
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error clearing table {e}")
