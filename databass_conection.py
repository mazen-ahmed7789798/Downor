"This Module is Connected To Database"

import sqlite3
from typing import Union, List, Tuple, Any

class DatabaseManager:
    """Database Manager Class"""
    
    def __init__(self, db_path : str):
        self.db = sqlite3.connect(db_path)
        self.cur = self.db.cursor()
    
    def close(self):
        """Close the database connection"""
        self.db.close()

    def commit(self):
        """Commit changes to the database"""
        self.db.commit()
    
    def is_new_user():
        """Check if No Users in Database"""
        cur.execute("SELECT name FROM user")
        if cur.fetchone is None:
            return True
        return False

    def import_data(
        self,
        table_name: str,
        many: Any | None = None,
        condition: Any | None = None,
        columns: str | list[Any] | tuple[Any, ...] = "all",
    ) -> str | list[Any]:
        if not table_name:
            return "Table Name is Required"
        
        # تحضير أسماء الأعمدة
        if columns == "all":
            cols = "*"
        else:
            if isinstance(columns, (list, tuple)):
                cols = ", ".join(columns)
            else:
                cols = columns
        
        try:
            # بناء الاستعلام
            if condition is not None:
                query = f"SELECT {cols} FROM {table_name} WHERE {condition}"
            else:
                query = f"SELECT {cols} FROM {table_name}"
                
            self.cur.execute(query)
            
            if many is not None:
                try:
                    many = int(many)
                    return self.cur.fetchmany(many)
                except ValueError:
                    return "The Many Param must be Integer"
            return self.cur.fetchall()
            
        except sqlite3.Error as e:
            return f"Error Happens, {e}"
    
    def create_table(
        self,
        table_name: str,
        columns: List[Tuple[str, str]]
    ) :

        """Create a new table in the database."""
        try:
            cols_with_types = ", ".join([f"{col} {dtype}" for col, dtype in columns])
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols_with_types})"
            self.cur.execute(query)
            self.db.commit()
            return f"Table {table_name} created successfully."
        except sqlite3.Error as e:
            return f"Error creating table: {str(e)}"

    def add_new_column(
        self,
        table_name: str,
        column_name: str,
        column_type: str,
        default_value: Any = None    
    ) -> str: 
        """ Add a new column to on existing table in the database."""
        try:
            if default_value is not None:
                query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} DEFAULT ?"
                self.cur.execute(query, (default_value,))
                self.db.commit()
            else:
                query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
                self.cur.execute(query)
                self.db.commit()
            return f"Column {column_name} added successfully to {table_name}."
        except sqlite3.Error as e:
            return f"Error adding column: {str(e)}"
            
    def inserting_data(
        self,
        table_name: str,
        columns: Union[str, List[str], Tuple[str, ...]],
        values: Union[str, List[str], Tuple[str, ...]]
    ) -> str:
        """Insert data into the database safely."""
        try:
            if isinstance(columns, str):
                # إذا كان columns نص واحد، نفترض أنه بالصيغة "(col1, col2)"
                cols = columns
            else:
                # إذا كان قائمة أو tuple، نحوله لنص
                cols = "(" + ", ".join(columns) + ")"
            
            # تحضير علامات الاستفهام بنفس عدد القيم
            if isinstance(values, (list, tuple)):
                placeholders = "(" + ", ".join(["?"] * len(values)) + ")"
                vals = tuple(values)
            else:
                # إذا كانت قيمة واحدة
                placeholders = "(?)"
                vals = (values,)
                
            query = f"INSERT INTO {table_name} {cols} VALUES {placeholders}"
            self.cur.execute(query, vals)
            self.commit()
            return "Data inserted successfully"
            
        except sqlite3.Error as e:
            return f"Error inserting data: {str(e)}"       

    def delete_table_data(
        self,
        table_name: str,
        condition: str | None = None
    ) -> str: 
        """Delete data from the database."""
        try :
            if condition:
                query = f"DELETE FROM {table_name} WHERE {condition}"
                self.cur.execute(query)
                self.commit()
            else :
                query = f"DELETE FROM {table_name}"
                self.cur.execute(query)
                self.commit()
            return "Data deleted successfully"
        except sqlite3.Error as e:
            return f"Error deleting data: {str(e)}"

    def delete_table(
        self,
        table_name: str 
    ) -> str:
        """ Delete a table from the database."""
        try :
            query = f"DROP TABLE IF EXISTS {table_name}"
            self.cur.execute(query)
            self.commit()
            return f"Table {table_name} deleted successfully."
        except sqlite3.Error as e:
            return f"Error deleting table: {str(e)}"

    def update_data(
        self,
        table_name: str,
        updates: List[Tuple[str, Any]],
        condition: str | None = None
    ) -> str:
        """ Updata data in the database."""
        try :
            set_clause = ", ".join([f"{col} = ?" for col, _ in updates])
            values = tuple(val for _, val in updates)
            
            if condition:
                query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            else:
                query = f"UPDATE {table_name} SET {set_clause}"
                
            self.cur.execute(query, values)
            self.commit()
            return "Data updated successfully"
        except sqlite3.Error as e:
            return f"Error updating data: {str(e)}"

    def get_table_info(
        self,
        table_name: str
    ) -> Union[str, List[Tuple]]:
        """ Get information about a table's structure."""
        try :
            query = f"PRAGMA table_info({table_name})"
            self.cur.execute(query)
            return self.cur.fetchall()
        except sqlite3.Error as e:
            return f"Error getting table info: {str(e)}"

