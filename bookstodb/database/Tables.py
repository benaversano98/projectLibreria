from FunzioniDB import *


def create_tables(connection):
    table_books = """
    CREATE TABLE books(
    id BIGINT PRIMARY KEY,
    title VARCHAR(1000) NOT NULL,
    author VARCHAR(1000),
    year_publication INT,
    url VARCHAR(1000),
    small_url VARCHAR(1000)
    )
    """

    table_users = """
       CREATE TABLE users(
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        date_of_birth DATE
        )
       """

    table_loan = """
       CREATE TABLE loan(
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        book_id BIGINT,
        user_id BIGINT,
        date_of_loan DATE
        )
       """

    alter_loan = """
               ALTER TABLE loan
               ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
               ADD FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE ON UPDATE CASCADE;
               """

    execute_query(connection, table_books)
    execute_query(connection, table_users)
    execute_query(connection, table_loan)
    execute_query(connection, alter_loan)
