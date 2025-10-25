# 2025/10/25 erb07
# (CT290DS007) 
# Certificate in Python Web Framework Devleopment Assistant
# Student Name: Antoninus Yeung CH
#
# Program: Applicaiton for data import / export / delete on PostgreSQL DB
# 
# Todo: Next version will be include the table schema for data validation
#
# >>>python db-tool.py 
#
# "clean_data": Clean code to be modify, suspense on 2025/10/20

import psycopg2
import csv
import os
import cmd
import logging

# Set up logging
logging.basicConfig(filename='db_tool.log', level=logging.ERROR)

class DatabaseTool(cmd.Cmd):
   intro = 'Welcome to the PostgreSQL Data Import/Export Tool. Type help or ? to list commands.'
   prompt = '(db-tool) '

   def __init__(self, host, port, dbname, user, password):
       super().__init__()
       self.conn = self.get_db_connection(host, port, dbname, user, password)

   def get_db_connection(self, host, port, dbname, user, password):
       """Establishes a connection to the PostgreSQL database."""
       try:
           conn = psycopg2.connect(
               host=host,
               port=port,
               dbname=dbname,
               user=user,
               password=password
           )
           return conn
       except psycopg2.Error as e:
           logging.error(f"Error connecting to database: {e}")
           print(f"Error connecting to database: {e}")
           exit(1)

   def do_export(self, arg):
       """Export data from a specified table to a CSV file.
       Usage: export <table_name> <output_file>
       """
       args = arg.split()
       if len(args) != 2:
           print("Usage: export <table_name> <output_file>")
           return

       table_name, output_file = args
       self.export_data(table_name, output_file)

   def export_data(self, table_name, output_file):
       """Exports data from a specified table to a CSV file."""
       try:
           with self.conn.cursor() as cur:
               cur.execute(f"SELECT * FROM {table_name}")
               rows = cur.fetchall()
               column_names = [desc[0] for desc in cur.description]

               with open(output_file, 'w', newline='') as f:
                   writer = csv.writer(f)
                   writer.writerow(column_names)  # Write header
                   writer.writerows(rows)
           print(f"Data from table '{table_name}' exported to '{output_file}' successfully.")
       except psycopg2.Error as e:
           print(f"Error exporting data: {e}")
           logging.error(f"Error exporting data: {e}")

   def do_import(self, arg):
       """Import data from a CSV file into a specified table.
       Usage: import <table_name> <input_file>
       """
       args = arg.split()
       if len(args) != 2:
           print("Usage: import <table_name> <input_file>")
           return

       table_name, input_file = args
       self.import_data(table_name, input_file)

#    def clean_data(self, row):
#        """Checks and cleans data in a row.
#        Validates email format, removes special characters, and applies additional checks.
#        Returns the cleaned row.
#        """
#        cleaned_row = []
#        for item in row:
#            # Check for empty strings
#            if item.strip() == '':
#                cleaned_row.append(None)  # Replace with None or a default value
#                continue
              
#            # Validate email format
#            if re.match(r"[^@]+@[^@]+\.[^@]+", item):
#                cleaned_row.append(item)  # Keep valid email
#                continue
              
#            # Validate numeric fields (example: check if item is a number)
#            if item.isdigit() and int(item) >= 0:  # Example: non-negative integers
#                cleaned_row.append(item)
#                continue
              
#            # Validate date format (example: YYYY-MM-DD)
#            if re.match(r"\d{4}-\d{2}-\d{2}", item):
#                cleaned_row.append(item)
#                continue
              
#            # Check for special characters and length (e.g., max length of 50)
#            if re.match(r"^[\w\s]+$", item) and len(item) <= 50:
#                cleaned_row.append(item)  # Keep valid characters
#                continue
              
#            # Replace invalid data with an empty string or None
#            cleaned_row.append(None)  # Or use '' depending on your use case

#        return cleaned_row
  
   def import_data(self, table_name, input_file):
       """Imports data from a CSV file into a specified table."""
       try:
           with open(input_file, 'r') as f:
               reader = csv.reader(f)
               header = next(reader)  # Read header row
               columns = ', '.join(header)
               placeholders = ', '.join(['%s'] * len(header))

               with self.conn.cursor() as cur:
                   for row in reader:
#                        cleaned_row = self.clean_data(row)  # Clean the row data
                       cleaned_row = row
                       cur.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", cleaned_row)
                   self.conn.commit()
           print(f"Data from '{input_file}' imported into table '{table_name}' successfully.")
       except psycopg2.Error as e:
           print(f"Error importing data: {e}")
           logging.error(f"Error importing data: {e}")
           self.conn.rollback()  # Rollback changes in case of error
       except FileNotFoundError:
           print(f"Error: Input file '{input_file}' not found.")
      

   def do_delete(self, arg):
       """Delete rows from a specified table based on a condition.
       Usage: delete <table_name> <condition>
       Example: delete users "id = 5"
       """
       args = arg.split(' ', 1)  # Split on first space
       if len(args) != 2:
           print("Usage: delete <table_name> <condition>")
           return

       table_name, condition = args
      
       # Confirmation prompt
       confirm = input(f"Are you sure you want to delete rows from '{table_name}' where {condition}? (yes/no): ")
       if confirm.lower() != 'yes':
           print("Deletion canceled.")
           return

       self.delete_rows(table_name, condition)

   def delete_rows(self, table_name, condition):
       """Deletes rows from the specified table based on the condition."""
       try:
           with self.conn.cursor() as cur:
               query = f"DELETE FROM {table_name} WHERE {condition}"
               cur.execute(query)
               self.conn.commit()
           print(f"Rows deleted from table '{table_name}' where {condition}.")
       except psycopg2.Error as e:
           print(f"Error deleting rows: {e}")
           logging.error(f"Error deleting rows: {e}")
           self.conn.rollback()  # Rollback changes in case of error

   def do_exit(self, arg):
       """Exit the tool."""
       print("Goodbye!")
       return True


  
def main():
   host = input("Enter database host (default: localhost): ") or 'localhost'
   port = input("Enter database port (default: 5432): ") or '5432'
   dbname = input("Enter database name: ")
   user = input("Enter database user: ")
   password = input("Enter database password: ")

   db_tool = DatabaseTool(host, port, dbname, user, password)
  
   try:
       db_tool.cmdloop()
   except KeyboardInterrupt:
       print("\nExiting the tool. Goodbye!")
       exit(0)

if __name__ == "__main__":
   main()

