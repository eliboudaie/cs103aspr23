import sqlite3

class Transaction:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            item_num INTEGER,
                            amount REAL,
                            category TEXT,
                            date TEXT,
                            description TEXT)''')
        self.conn.commit()

    def add_transaction(self, item_num, amount, category, date, description):
        self.cursor.execute('''INSERT INTO transactions (item_num, amount, category, date, description)
                            VALUES (?, ?, ?, ?, ?)''', (item_num, amount, category, date, description))
        self.conn.commit()

    def get_categories(self):
        self.cursor.execute('''SELECT category FROM transactions''')
        rows = self.cursor.fetchall()
        return rows

    def modify_category(self, old, new):
        self.cursor.execute('''UPDATE transactions SET category=? WHERE category=?''', (new, old))

    def get_transactions(self):
        self.cursor.execute('''SELECT * FROM transactions''')
        rows = self.cursor.fetchall()
        return rows

    def get_transaction_by_id(self, id):
        self.cursor.execute('''SELECT * FROM transactions WHERE id = ?''', (id,))
        row = self.cursor.fetchone()
        return row

    def update_transaction(self, id, item_num, amount, category, date, description):
        self.cursor.execute('''UPDATE transactions SET item_num = ?, amount = ?, category = ?, date = ?, description = ?
                            WHERE id = ?''', (item_num, amount, category, date, description, id))
        self.conn.commit()

    def delete_transaction(self, id):
        self.cursor.execute('''DELETE FROM transactions WHERE id = ?''', (id,))
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
    def summarize_by_month(self, year):
            """Summarizes transactions by month for a given year"""
            query = """
                SELECT 
                    strftime('%m', date) AS month, 
                    sum(amount) AS total 
                FROM 
                    transactions 
                WHERE 
                    strftime('%Y', date) = ? 
                GROUP BY 
                    month 
                ORDER BY 
                    month ASC
            """
            self.cursor.execute(query, (year,))
            return self.cursor.fetchall()

    def summarize_by_year(self):
        """Summarizes transactions by year"""
        query = """
            SELECT 
                strftime('%Y', date) AS year, 
                sum(amount) AS total 
            FROM 
                transactions 
            GROUP BY 
                year 
            ORDER BY 
                year ASC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def summarize_by_date(self, start_date, end_date):
        """Summarizes transactions by date range"""
        query = """
            SELECT 
                date, 
                sum(amount) AS total 
            FROM 
                transactions 
            WHERE 
                date BETWEEN ? AND ? 
            GROUP BY 
                date 
            ORDER BY 
                date ASC
        """
        self.cursor.execute(query, (start_date, end_date))
        return self.cursor.fetchall()

    def summarize_by_category(self, category):
        """Summarizes transactions by category"""
        query = """
            SELECT 
                category, 
                sum(amount) AS total 
            FROM 
                transactions 
            WHERE 
                category = ? 
            GROUP BY 
                category
        """
        self.cursor.execute(query, (category,))
        return self.cursor.fetchall()