import psycopg2

conn = psycopg2.connect(
    dbname="test",
    user="postgres",
    password="aty",
    host="localhost",
    port="5432"
)

conn.autocommit = True  # Set to True for immediate command execution
cursor = conn.cursor()

sql_file_path = "database_dump.sql"

try:
    with open(sql_file_path, 'r') as f:
        sql_commands = f.read()
    cursor.execute(sql_commands)
    print(f"Successfully imported data from {sql_file_path}")
except psycopg2.Error as e:
    print(f"Error importing data: {e}")
finally:
    cursor.close()
    conn.close()