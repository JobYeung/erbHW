# db-tool and createPostgresDB 

1. db-tool.py
2. createPostgresDB.py

Command Line Applicaiton "db-tool.py", which can import, export and delete the data in PostgreSQL Database. 

Command Line Applicaiton "createPostgresDB.py", which can crate the database in PostgreSQL.


## Installation 

Command line tools are no need to install but need the pip (intall) the relative packages/library to perform the tools.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install relative package to run the tools.

```bash
pip intall os psycopg2 logging sqlparse
```

## Usage

**db-tool**.py for data import/export/delete

```bash
python db-tool.py 
```

#### Interactive mode
```bash
Enter database host (default: localhost):  
Enter database port (default: 5432): 
Enter database name: 
Enter database user: 
Enter database password: 
Welcome to the PostgreSQL Data Import/Export Tool. Type help or ? to list commands.
(db-tool) ?

Documented commands (type help <topic>):
========================================
delete  exit  export  help  import

(db-tool) 

```

___

***createPostgresDB***.py for database creation in PostgreSQL

```bash
python createPostgresDB.py 
```

edit the **createPostgresDB**.py params to perform the program, change the DB_NAME, PG_USER, and PG_PASSWORD as yours.
```python
if __name__ == "__main__":
    # Replace with your PostgreSQL credentials and desired database name
    DB_NAME = "DBNAME"
    PG_USER = "postgres"  # Default PostgreSQL user
    PG_PASSWORD = "***" # Replace with your actual password

    create_postgresql_database(DB_NAME, PG_USER, PG_PASSWORD)
```
## Pending 

***createMultiDB***.py is pending develop.
This tools will be include database creation for PostgreSQL, sqlite, MySQL, and MongoDB as well as create tables by schema.json.

2025/10/25 PostgreSQL done.

## Supplements

### florist1.csv, product1.csv, taggit_tag1.csv, taggit_taggeditems1.csv
The above ***4 files*** are testing data. Feel free to use.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)