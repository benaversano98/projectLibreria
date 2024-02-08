from FunzioniDB import *
def create_tables(connection):
    table_books = """
    CREATE TABLE books(
    isbn BIGINT PRIMARY KEY,
    book_Title VARCHAR(1000) NOT NULL,
    book_Author VARCHAR(1000),
    year_publication VARCHAR(1000), 
    publisher VARCHAR(1000))
    """

    table_img = """
    CREATE TABLE images(
    isbn BIGINT PRIMARY KEY,
    url VARCHAR(1000))
    """

    alter_img = '''
       ALTER TABLE images
       ADD FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE ON UPDATE CASCADE;'''

    execute_query(connection, table_books)
    execute_query(connection, table_img)
    execute_query(connection, alter_img)