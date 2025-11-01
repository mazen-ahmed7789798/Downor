"This Module is Connected To Database"

import sqlite3
from typing import Union, List, Tuple
from typing import Any



db = sqlite3.connect("DownloadManager.db")
cur = db.cursor()
# Create Tables
cur.execute(
    """
            CREATE TABLE IF NOT EXISTS downloads (title TEXT,
            url TEXT,
            downloaded DateTime,
            type TEXT
            file_path TEXT
            thumbnail BLOB)
            """
)


# Is New User Function
def is_new_user():

    cur.execute("SELECT name FROM user")
    if cur.fetchone is None:
        return True
    else:
        return False


# import data from table
def import_data(
    table_name: str,
    many: Any | None = None,
    condition: Any | None = None,
    columns: str | list[Any] | tuple[Any, ...] = "all",
) -> str | list[Any]:
    """This Function is used to import data from database
    `Table Name `: This A Table Name Which Will Get The Data From It
    `Many`: This How Many Row You Want To Get It (Not Necessary)"""
    # Table Name Condition
    if not table_name:
        return "Table Name is Required"
    # Columns Param Condition
    if columns == "all":
        columns = "*"
    else:
        columns = tuple(columns)

    # Condition Param Condition
    if condition is not None:
        if not isinstance(condition, str):
            return "Condition Param must be String"
        else:
            try:
                cur.execute(
                    "SELECT ? FROM ? WHERE ? ", (columns, table_name, condition)
                )
            except sqlite3.Error as e:
                return f"Error Happens, {e}"
    else:
        try:
            cur.execute(f"SELECT {','.join(columns)} FROM {table_name}")
        except sqlite3.Error as e:
            return f"Error Happens, {e}"
    # Many Param Condition
    if many is None:
        return cur.fetchall()
    else:
        try:
            int(many)
        except ValueError:
            return "The Many Param must be Integer"
        else:
            many = int(many)
            return cur.fetchmany(many)



def inserting_data(
    table_name: str,
    columns: Union[str, List[str], Tuple[str, ...]],
    values: Union[str, List[str], Tuple[str, ...]]
) -> None:
    """Insert data into the database safely."""
    if isinstance(columns, (list, tuple)):
        cols = "(" + ", ".join(columns) + ")"
        placeholders = "(" + ", ".join(["?"] * len(values)) + ")"
        if not isinstance(values, tuple):
            values = tuple(values)
        try:
            cur.execute(
                f"INSERT INTO {table_name} {cols} VALUES {placeholders}", values
            )
            db.commit()
        except Exception as e:
            print(e)
    else:
        print("Columns should be a list or tuple.")


if __name__ == "__main__":

    import Downloader_manager # type:ignore
