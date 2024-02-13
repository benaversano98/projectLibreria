import mysql.connector
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Configura la connessione al database MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Libreria_Gruppo3'}


def create_db_connection():
    return mysql.connector.connect(**db_config)


# Funzione per eseguire query SQL
def execute_query(query, params=None, dictionary=True):
    connection = create_db_connection()
    if dictionary:
        cursor = connection.cursor(dictionary=True)
    else:
        cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


@app.route("/", methods=['GET', 'POST'])
def homepage():
    flag = True
    list_books = api_books()
    if request.method == 'POST':
        flag = False
        codice = request.form.get('Search')
        if codice:
            list_books = execute_query(
                f"SELECT * FROM books WHERE title LIKE '%{codice}%' OR author LIKE '%{codice}%'")
    image, frase = "https://img00.deviantart.net/9088/i/2007/223/7/d/no_books_by_applejoan.jpg", "Non ci sono libri a questa ricerca."
    return render_template("home.html", image=image, frase=frase, list_books=list_books, len=len, flag=flag)


@app.route("/api/books")
def api_books():
    query_lg = f'SELECT * FROM books'
    list_books = execute_query(query_lg)
    return list_books


@app.route("/api/users")
def api_users():
    query_lg = 'SELECT * FROM users'
    list_users = execute_query(query_lg)
    return jsonify(list_users)


@app.route("/api/loan")
def api_loan():
    query_lg = 'SELECT * FROM loan'
    list_loan = execute_query(query_lg)
    return jsonify(list_loan)


@app.route("/loan")
def loan():
    query = """
    SELECT users.name, GROUP_CONCAT(books.title SEPARATOR ", ") AS title, GROUP_CONCAT(loan.date_of_loan SEPARATOR ", ") AS date_loan
    FROM loan JOIN users JOIN books
    ON loan.book_id = books.id AND loan.user_id=users.id
    GROUP BY users.name;
    """
    list_loan = execute_query(query)
    # return jsonify(list_loan)
    return render_template("prestiti.html", list_loan=list_loan)


if __name__ == '__main__':
    app.run(debug=True)
