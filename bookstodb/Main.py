from Tables import *
from Libri_CSV_DB import *
from Utenti_CSV_DB import *
from Prestiti_CSV_DB import *

host = "localhost"
user = "root"
pw = ""
db = "Libreria_Gruppo3"
file_csv = 'books.csv'

connection = create_server_connection(host, user, pw)
execute_query(connection, f"DROP DATABASE IF EXISTS {db}")
create_database(connection, "CREATE DATABASE %s" % db)
# Connettiti al database
connection = create_db_connection(host, user, pw, db)
create_tables(connection)
libri_to_DB("books.csv", connection)
utenti_to_DB("users.csv", connection)
prestiti_to_DB("loan.csv", connection)

