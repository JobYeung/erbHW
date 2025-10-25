import psycopg2
from psycopg2 import sql
import sqlite3
import mysql.connector
import json
from pymongo import MongoClient

#
# ### Table Schema: JSON file sample 
# 
# {
#     "table_name": "users",
#     "columns": [
#         {"name": "id", "type": "serial", "primary_key": true},
#         {"name": "name", "type": "varchar(100)", "nullable": false},
#         {"name": "email", "type": "varchar(100)", "nullable": false},
#         {"name": "age", "type": "int", "nullable": true},
#         {"name": "is_active", "type": "boolean", "default": true}
#     ]
# }

def create_postgresql_database(db_name, user, password, host='localhost', port=5432):
    """Connects to a PostgreSQL instance and creates a new database."""
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            database="postgres",
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
        cursor.execute(create_db_query)
        print(f"Database '{db_name}' created successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_sqlite_database(db_name):
    """Creates a new SQLite database."""
    conn = sqlite3.connect(f"{db_name}.db")
    print(f"SQLite database '{db_name}.db' created successfully.")
    conn.close()

def create_mysql_database(db_name, user, password, host='localhost', port=3306):
    """Connects to a MySQL instance and creates a new database."""
    try:
        conn = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"MySQL database '{db_name}' created successfully.")
    except mysql.connector.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_mongodb_database(db_name):
    """Creates a new MongoDB database."""
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    print(f"MongoDB database '{db_name}' created successfully.")

def import_schema_postgresql(db_name, user, password, schema_file):
    """Import table schema into PostgreSQL."""
    with open(schema_file, 'r') as f:
        schema = json.load(f)

    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            database=db_name,
            user=user,
            password=password
        )
        cursor = conn.cursor()

        table_name = schema['table_name']
        columns = []
        for column in schema['columns']:
            col_def = f"{column['name']} {column['type']}"
            if column.get('primary_key'):
                col_def += " PRIMARY KEY"
            if not column.get('nullable', True):
                col_def += " NOT NULL"
            if 'default' in column:
                col_def += f" DEFAULT {column['default']}"
            columns.append(col_def)

        create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)});"
        cursor.execute(create_table_query)
        conn.commit()
        print(f"Table '{table_name}' created in PostgreSQL database '{db_name}'.")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def import_schema_sqlite(db_name, schema_file):
    """Import table schema into SQLite."""
    conn = sqlite3.connect(f"{db_name}.db")
    with open(schema_file, 'r') as f:
        schema = json.load(f)

    table_name = schema['table_name']
    columns = []
    for column in schema['columns']:
        col_def = f"{column['name']} {column['type']}"
        if not column.get('nullable', True):
            col_def += " NOT NULL"
        if 'default' in column:
            col_def += f" DEFAULT {column['default']}"
        columns.append(col_def)

    create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)});"
    conn.execute(create_table_query)
    conn.commit()
    print(f"Table '{table_name}' created in SQLite database '{db_name}.db'.")
    conn.close()

def import_schema_mysql(db_name, user, password, schema_file):
    """Import table schema into MySQL."""
    conn = mysql.connector.connect(user=user, password=password, host='localhost', database=db_name)
    cursor = conn.cursor()
    with open(schema_file, 'r') as f:
        schema = json.load(f)

    table_name = schema['table_name']
    columns = []
    for column in schema['columns']:
        col_def = f"{column['name']} {column['type']}"
        if not column.get('nullable', True):
            col_def += " NOT NULL"
        if 'default' in column:
            col_def += f" DEFAULT {column['default']}"
        columns.append(col_def)

    create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)});"
    cursor.execute(create_table_query)
    conn.commit()
    print(f"Table '{table_name}' created in MySQL database '{db_name}'.")
    cursor.close()
    conn.close()

def import_schema_mongodb(db_name, schema_file):
    """Import table schema into MongoDB."""
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    
    with open(schema_file, 'r') as f:
        schema = json.load(f)

    # MongoDB is schema-less, but you can create a collection
    db.create_collection(schema['table_name'])
    print(f"Collection '{schema['table_name']}' created in MongoDB database '{db_name}'.")

def main():
    try:
        db_type = input("Enter database type (postgresql, sqlite, mysql, mongodb): ").strip().lower()

        if db_type == "postgresql":
            user = input("Enter PostgreSQL username: ")
            password = input("Enter PostgreSQL password: ")
            db_name = input("Enter the name of the database to create: ")
            create_postgresql_database(db_name, user, password)
            schema_file = input("Enter the path to the schema file: ")
            import_schema_postgresql(db_name, user, password, schema_file)

        elif db_type == "sqlite":
            db_name = input("Enter the name of the SQLite database to create: ")
            create_sqlite_database(db_name)
            schema_file = input("Enter the path to the schema file: ")
            import_schema_sqlite(db_name, schema_file)

        elif db_type == "mysql":
            user = input("Enter MySQL username: ")
            password = input("Enter MySQL password: ")
            db_name = input("Enter the name of the database to create: ")
            create_mysql_database(db_name, user, password)
            schema_file = input("Enter the path to the schema file: ")
            import_schema_mysql(db_name, user, password, schema_file)

        elif db_type == "mongodb":
            db_name = input("Enter the name of the MongoDB database to create: ")
            create_mongodb_database(db_name)
            schema_file = input("Enter the path to the schema file: ")
            import_schema_mongodb(db_name, schema_file)

        else:
            print("Unsupported database type.")
    
    except KeyboardInterrupt:
        print("\nGoodbye!")
        exit(0)

if __name__ == "__main__":
    main()