import psycopg2
import os

# Database connection details
DB_NAME = "test"
DB_USER = "postgres"
DB_HOST = "localhost"  # Or your remote host
DB_PORT = "5432"
DB_PASSWORD = "aty"  # Consider using environment variables for security

# Output file path for the dump
OUTPUT_FILE = "database_dump.sql"

def dump_database():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = connection.cursor()
        
        # Open the output file to write the dump
        with open(OUTPUT_FILE, 'w') as output_file:
            # Fetch all tables for dumping
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                # Dump table structure
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()
                output_file.write(f"-- Dumping table: {table_name}\n")
                for row in rows:
                    output_file.write(f"INSERT INTO {table_name} VALUES {row};\n")
                output_file.write("\n")

        print(f"Database '{DB_NAME}' dumped successfully to '{OUTPUT_FILE}'")

    except Exception as e:
        print(f"Error dumping database: {e}")
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    dump_database()