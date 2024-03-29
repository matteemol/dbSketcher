import sqlite3
import sys
from sqlite3 import Error


def execute_script(sqlite_db, scriptFile):
    """
Runs an SQLite script from a file.

`sqlite_db`: the .sqlite database (created if doesn't exists)
`scriptFile`: the file with the script to run on `sqlite_db`
"""
    try:
        sqliteConnection = sqlite3.connect(sqlite_db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        with open(scriptFile, 'r') as sqlite_file:
            sql_script = sqlite_file.read()

        cursor.executescript(sql_script)
        print("SQLite script executed successfully")
        cursor.close()

    except Error as e:
        print(f"The error '{e}' occurred")

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Wrong number of arguments")
        print("python3 sqlitegen.py <sql script file>")
        exit()

    file = sys.argv[1]

    execute_script(f"{file[:-4]}.sqlite", file)