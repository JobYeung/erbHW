import psycopg2
from psycopg2 import sql

def create_postgresql_database(db_name, user, password, host='localhost', port=5432):
    """
    Connects to a PostgreSQL instance and creates a new database.

    Args:
        db_name (str): The name of the database to create.
        user (str): The PostgreSQL username.
        password (str): The PostgreSQL password.
        host (str, optional): The PostgreSQL host. Defaults to 'localhost'.
        port (int, optional): The PostgreSQL port. Defaults to 5432.
    """
    conn = None
    cursor = None
    try:
        # Connect to the default 'postgres' database to create a new one
        conn = psycopg2.connect(
            database="postgres",
            user=user,
            password=password,
            host=host,
            port=port
        )

        # Set autocommit to True for CREATE DATABASE to work outside a transaction block
        conn.autocommit = True
        cursor = conn.cursor()

        # Construct the CREATE DATABASE query
        create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))

        # Execute the query
        cursor.execute(create_db_query)
        print(f"Database '{db_name}' created successfully.")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Replace with your PostgreSQL credentials and desired database name
    DB_NAME = "blossom"
    PG_USER = "postgres"  # Default PostgreSQL user
    PG_PASSWORD = "aty" # Replace with your actual password

    create_postgresql_database(DB_NAME, PG_USER, PG_PASSWORD)