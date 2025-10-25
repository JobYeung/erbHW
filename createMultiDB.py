# 2025/10/25 erb07
# (CT290DS007) 
# Certificate in Python Web Framework Devleopment Assistant
# Student Name: Antoninus Yeung CH
#
# Program: Applicaiton for table creation on PostgreSQL DB, MySQL, sqlite, MongoDB
# 
# 
# >>>python createMultiDB.py 
#
# ### file name: schema.json
# {
#     "tables": [
#         {
#             "table_name": "users",
#             "columns": [
#                 {"name": "id", "type": "serial", "primary_key": true},
#                 {"name": "name", "type": "varchar(100)", "nullable": false},
#                 {"name": "email", "type": "varchar(100)", "nullable": false},
#                 {"name": "age", "type": "int", "nullable": true},
#                 {"name": "is_active", "type": "boolean", "default": true}
#             ]
#         },
#         {
#             "table_name": "posts",
#             "columns": [
#                 {"name": "id", "type": "serial", "primary_key": true},
#                 {"name": "title", "type": "varchar(200)", "nullable": false},
#                 {"name": "content", "type": "text", "nullable": false},
#                 {"name": "user_id", "type": "int", "nullable": false, "foreign_key": "users(id)"}
#             ]
#         }
#     ]
# }

import psycopg2
from psycopg2 import sql
import sqlite3
import mysql.connector
import json
import logging
import os
from pymongo import MongoClient

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filename='db_tool.log',)

VALID_DATA_TYPES = {
    "serial": "serial",
    "varchar": "varchar",
    "int": "int",
    "boolean": "boolean",
    "text": "text",
    "date": "date",
    "timestamp": "timestamp"
}

def database_exists_postgresql(db_name, user, password, host='localhost', port=5432):
    """Check if a PostgreSQL database exists."""
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(database="postgres", user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
        return cursor.fetchone() is not None
    except psycopg2.Error as e:
        logging.error(f"Error checking if database exists: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def database_exists_sqlite(db_name):
    """Check if a SQLite database exists."""
    return os.path.isfile(f"{db_name}.db")

def database_exists_mysql(db_name, user, password, host='localhost', port=3306):
    """Check if a MySQL database exists."""
    try:
        conn = mysql.connector.connect(user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES LIKE %s;", (db_name,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as e:
        logging.error(f"Error checking if database exists: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_postgresql_database(db_name, user, password, host='localhost', port=5432):
    """Connects to a PostgreSQL instance and creates a new database."""
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(database="postgres", user=user, password=password, host=host, port=port)
        conn.autocommit = True
        cursor = conn.cursor()

        create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
        cursor.execute(create_db_query)
        logging.info(f"Database '{db_name}' created successfully.")

    except psycopg2.OperationalError as e:
        logging.error(f"Operational error: {e}")
        if "peer authentication failed" in str(e):
            logging.error("Peer authentication failed. Please check your PostgreSQL user settings.")
    except psycopg2.Error as e:
        logging.error(f"An error occurred while creating the database: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_sqlite_database(db_name):
    """Creates a new SQLite database."""
    conn = sqlite3.connect(f"{db_name}.db")
    logging.info(f"SQLite database '{db_name}.db' created successfully.")
    conn.close()

def create_mysql_database(db_name, user, password, host='localhost', port=3306):
    """Connects to a MySQL instance and creates a new database."""
    try:
        conn = mysql.connector.connect(user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {db_name}")
        logging.info(f"MySQL database '{db_name}' created successfully.")
    except mysql.connector.Error as e:
        logging.error(f"An error occurred while creating the database: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_mongodb_database(db_name):
    """Creates a new MongoDB database."""
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    logging.info(f"MongoDB database '{db_name}' created successfully.")

def validate_data_type(data_type):
    """Validate the data type against the allowed types."""
    if data_type not in VALID_DATA_TYPES:
        raise ValueError(f"Invalid data type: {data_type}. Allowed types are: {', '.join(VALID_DATA_TYPES.keys())}")

def validate_schema(schema):
    """Validate the schema structure."""
    if 'tables' not in schema:
        raise ValueError("Schema must have a 'tables' key.")
    
    for table in schema['tables']:
        if 'table_name' not in table or 'columns' not in table:
            raise ValueError("Each table must have 'table_name' and 'columns' keys.")
        
        for column in table['columns']:
            if 'name' not in column or 'type' not in column:
                raise ValueError("Each column must have 'name' and 'type' keys.")
            validate_data_type(column['type'])

def import_schema_postgresql(db_name, user, password, schema_file):
    """Import table schema into PostgreSQL."""
    logging.info(f"DBN:{db_name} UID:{user} Schema: {schema_file}")
    if not os.path.isfile(schema_file):
        logging.error(f"Schema file '{schema_file}' does not exist.")
        return

    try:
        with open(schema_file, 'r') as f:
            schema = json.load(f)
    except json.JSONDecodeError:
        logging.error(f"Schema file '{schema_file}' is not valid JSON.")
        return

    validate_schema(schema)

    # logging.info(f"2. DBN:{db_name} UID:{user} Schema: {schema_file}")
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(database=db_name, user=user, password=password, host="localhost")
        cursor = conn.cursor()
        # logging.info(f"3. DBN:{db_name} UID:{user} Schema: {schema_file}")
        for table in schema['tables']:
            table_name = table['table_name']
            columns = []
            foreign_keys = []

            for column in table['columns']:
                col_def = f"{column['name']} {column['type']}"
                if column.get('primary_key'):
                    col_def += " PRIMARY KEY"
                if not column.get('nullable', True):
                    col_def += " NOT NULL"
                if 'default' in column:
                    col_def += f" DEFAULT {column['default']}"
                
                columns.append(col_def)

                # Handle foreign keys
                if 'foreign_key' in column:
                    foreign_keys.append(f"FOREIGN KEY ({column['name']}) REFERENCES {column['foreign_key']}")

            create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)}{', ' + ', '.join(foreign_keys) if foreign_keys else ''});"
            logging.info(f"Table Create: {create_table_query}")
            try:
                cursor.execute(create_table_query)
                conn.commit()
                logging.info(f"Table '{table_name}' created in PostgreSQL database '{db_name}'.")
            except psycopg2.Error as e:
                logging.error(f"Error creating table '{table_name}': {e}")
                conn.rollback()

    except (psycopg2.Error, ValueError) as e:
        logging.error(f"An error occurred while importing the schema: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def import_schema_sqlite(db_name, schema_file):
    """Import table schema into SQLite."""
    if not os.path.isfile(schema_file):
        logging.error(f"Schema file '{schema_file}' does not exist.")
        return

    try:
        with open(schema_file, 'r') as f:
            schema = json.load(f)
    except json.JSONDecodeError:
        logging.error(f"Schema file '{schema_file}' is not valid JSON.")
        return

    validate_schema(schema)

    conn = sqlite3.connect(f"{db_name}.db")

    for table in schema['tables']:
        table_name = table['table_name']
        columns = []
        foreign_keys = []

        for column in table['columns']:
            col_def = f"{column['name']} {column['type']}"
            if not column.get('nullable', True):
                col_def += " NOT NULL"
            if 'default' in column:
                col_def += f" DEFAULT {column['default']}"
            
            columns.append(col_def)

            # Handle foreign keys
            if 'foreign_key' in column:
                foreign_keys.append(f"FOREIGN KEY ({column['name']}) REFERENCES {column['foreign_key']}")

        create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)}{', ' + ', '.join(foreign_keys) if foreign_keys else ''});"
        try:
            conn.execute(create_table_query)
            conn.commit()
            logging.info(f"Table '{table_name}' created in SQLite database '{db_name}.db'.")
        except sqlite3.Error as e:
            logging.error(f"Error creating table '{table_name}': {e}")
            conn.rollback()

    conn.close()

def import_schema_mysql(db_name, user, password, schema_file):
    """Import table schema into MySQL."""
    if not os.path.isfile(schema_file):
        logging.error(f"Schema file '{schema_file}' does not exist.")
        return

    try:
        with open(schema_file, 'r') as f:
            schema = json.load(f)
    except json.JSONDecodeError:
        logging.error(f"Schema file '{schema_file}' is not valid JSON.")
        return

    validate_schema(schema)

    conn = mysql.connector.connect(user=user, password=password, host='localhost', database=db_name)
    cursor = conn.cursor()

    for table in schema['tables']:
        table_name = table['table_name']
        columns = []
        foreign_keys = []

        for column in table['columns']:
            col_def = f"{column['name']} {column['type']}"
            if not column.get('nullable', True):
                col_def += " NOT NULL"
            if 'default' in column:
                col_def += f" DEFAULT {column['default']}"
            
            columns.append(col_def)

            # Handle foreign keys
            if 'foreign_key' in column:
                foreign_keys.append(f"FOREIGN KEY ({column['name']}) REFERENCES {column['foreign_key']}")

        create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)}{', ' + ', '.join(foreign_keys) if foreign_keys else ''});"
        try:
            cursor.execute(create_table_query)
            conn.commit()
            logging.info(f"Table '{table_name}' created in MySQL database '{db_name}'.")
        except mysql.connector.Error as e:
            logging.error(f"Error creating table '{table_name}': {e}")
            conn.rollback()

    cursor.close()
    conn.close()

def import_schema_mongodb(db_name, schema_file):
    """Import table schema into MongoDB."""
    if not os.path.isfile(schema_file):
        logging.error(f"Schema file '{schema_file}' does not exist.")
        return

    try:
        with open(schema_file, 'r') as f:
            schema = json.load(f)
    except json.JSONDecodeError:
        logging.error(f"Schema file '{schema_file}' is not valid JSON.")
        return

    validate_schema(schema)

    # MongoDB is schema-less, but you can create collections
    client = MongoClient('localhost', 27017)
    db = client[db_name]

    for table in schema['tables']:
        db.create_collection(table['table_name'])
        logging.info(f"Collection '{table['table_name']}' created in MongoDB database '{db_name}'.")

def main():
    try:
        db_type = input("Enter database type (postgresql, sqlite, mysql, mongodb): ").strip().lower()
        db_name = input("Enter the name of the database to create: ")

        if db_type == "postgresql":
            user = input("Enter PostgreSQL username: ")
            password = input("Enter PostgreSQL password: ")

            if database_exists_postgresql(db_name, user, password):
                logging.info(f"Database '{db_name}' already exists.")
                schema_file = input("Enter the path to the schema file to create tables: ")
                import_schema_postgresql(db_name, user, password, schema_file)
            else:
                create_postgresql_database(db_name, user, password)
                schema_file = input("Enter the path to the schema file to create tables: ")
                import_schema_postgresql(db_name, user, password, schema_file)

        elif db_type == "sqlite":
            if database_exists_sqlite(db_name):
                logging.info(f"Database '{db_name}.db' already exists.")
                schema_file = input("Enter the path to the schema file to create tables: ")
                import_schema_sqlite(db_name, schema_file)
            else:
                create_sqlite_database(db_name)
                schema_file = input("Enter the path to the schema file to create tables: ")
                import_schema_sqlite(db_name, schema_file)

        elif db_type == "mysql":
            user = input("Enter MySQL username: ")
            password = input("Enter MySQL password: ")

            if database_exists_mysql(db_name, user, password):
                logging.info(f"Database '{db_name}' already exists.")
                schema_file = input("Enter the path to the schema file to create tables: ")
                import_schema_mysql(db_name, user, password, schema_file)
            else:
                create_mysql_database(db_name, user, password)
                schema_file = input("Enter the path to the schema file to create tables: ")
                import_schema_mysql(db_name, user, password, schema_file)

        elif db_type == "mongodb":
            if database_exists_mongodb(db_name):
                logging.info(f"Database '{db_name}' already exists.")
                schema_file = input("Enter the path to the schema file to create collections: ")
                import_schema_mongodb(db_name, schema_file)
            else:
                create_mongodb_database(db_name)
                schema_file = input("Enter the path to the schema file to create collections: ")
                import_schema_mongodb(db_name, schema_file)

        else:
            logging.error("Unsupported database type.")
    
    except KeyboardInterrupt:
        logging.info("Goodbye!")
        exit(0)

if __name__ == "__main__":
    main()