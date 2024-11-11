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


    def close(self):
        if self.conn:
            self.conn.close()

    def __str__(self):
        try:
            self.cursor.execute('''SELECT * FROM fridge''')
            rows = self.cursor.fetchall()
            if rows:
                return '\n'.join([f"ID: {row[0]}, Name: {row[1]}, Quantity: {row[2]}, Unit: {row[3]}, Expiry: {row[4]}" for row in rows])
            else:
                return "No items in fridge"
        except sqlite3.Error as e: 
            print(f"Error fetching data {e}")
            return "Error fetching data"
    
