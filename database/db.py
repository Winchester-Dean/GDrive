import sqlite3

class DataBase:
    def __init__(
        self,
        directory: str = "database/database.db"
    ):
        self.connect = sqlite3.connect(directory)
        self.cursor = self.connect.cursor()

        with self.connect:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins(
                    id INTEGER PRIMARY KEY,
                    admin_id INTEGER NOT NULL,
                    name TEXT NOT NULL
                )
            """)
        
        with self.connect:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS domains(
                    id INTEGER PRIMARY KEY,
                    domain TEXT NOT NULL
                )
            """)
    
    def add_admin(self, admin_id: int, name: str):
        with self.connect:
            self.cursor.execute(
                "INSERT INTO admins(admin_id, name) "
                "VALUES(?, ?)",
                [admin_id, name]
            )
    
    def add_domain(self, domain: str):
        with self.connect:
            self.cursor.execute(
                "INSERT INTO domains(domain) "
                "VALUES(?)",
                [domain]
            )
    
    def get_admins(self):
        self.cursor.execute(
            "SELECT admin_id, name FROM admins"
        )
        return self.cursor.fetchall()
    
    def get_admins_id(self):
        self.cursor.execute(
            "SELECT admin_id FROM admins"
        )
        return self.cursor.fetchall()
    
    def get_domains(self):
        self.cursor.execute(
            "SELECT domain FROM domains"
        )
        return self.cursor.fetchall()

