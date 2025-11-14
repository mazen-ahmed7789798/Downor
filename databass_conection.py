"This Module is Connected To Database"

import sqlite3
from typing import Union, List, Tuple
from typing import Any



db = sqlite3.connect("DownloadManager.db")
cur = db.cursor()
# Create Tables
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS downloads (
        title TEXT,
        url TEXT,
        downloaded DateTime,
        type TEXT,
        file_path TEXT,
        thumbnail BLOB
    )
    """
)


# Is New User Function
def is_new_user():

    cur.execute("SELECT name FROM user")
    if cur.fetchone is None:
        return True
    else:
        return False


def import_data(
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
            
        cur.execute(query)
        
        if many is not None:
            try:
                many = int(many)
                return cur.fetchmany(many)
            except ValueError:
                return "The Many Param must be Integer"
        return cur.fetchall()
        
    except sqlite3.Error as e:
        return f"Error Happens, {e}"

def inserting_data(
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
        cur.execute(query, vals)
        db.commit()
        return "Data inserted successfully"
        
    except sqlite3.Error as e:
        return f"Error inserting data: {str(e)}"
if __name__ == "__main__":

    import Downloader_manager # type:ignore
