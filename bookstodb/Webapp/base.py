import mysql.connector
from flask import Flask, jsonify, render_template

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


################################ HOME HOME HOME HOME HOME HOME HOME HOME HOME HOME HOME  ##############################
@app.route("/")
def homepage():
    # ### NEW RELEASES ###
    # new_releases = {6: "https://www.liberta.it/wp-content/uploads/2021/10/midnight-mass-copertina-1232.jpg",
    #                 1291: 'https://images.squarespace-cdn.com/content/v1/57a21fc59de4bb8f9ae746d6/1613771670035-HKX2DZCQ2OWVJFSFWAH0/I+Care+A+lot_horizontal.jpg?format=1500w',
    #                 110: 'https://miro.medium.com/v2/resize:fit:1200/1*o3V9Pg__yNYc1FwJI-Yszg.jpeg'}
    #
    # query_nr = f'SELECT show_id, type, title, duration FROM `shows` WHERE show_id IN {tuple(new_releases.keys())};'
    # carousel = execute_query(query_nr)
    # for elem in carousel:
    #     elem.update({'src': new_releases[elem['show_id']]})
    #
    # ### TOP SELECT ###
    # query_tst = "SELECT type FROM `shows` GROUP BY type ORDER BY RAND() LIMIT 1;"
    # top_selected_type = execute_query(query_tst)[0]['type']
    # query_tsc = f"""
    # SELECT shows.show_id, shows.title, shows.rating,
    # GROUP_CONCAT(DISTINCT categories.category_name SEPARATOR ', ') AS 'categories'
    # FROM shows JOIN showcategories JOIN categories
    # ON shows.show_id = showcategories.show_id AND showcategories.category_id = categories.category_id
    # WHERE shows.type = '{top_selected_type}' GROUP BY shows.show_id ORDER BY RAND() LIMIT 4;
    # """
    # top_selected_content = execute_query(query_tsc)
    #
    # ### OUR RECOMENDATION ###
    # query_rgt = "SELECT * FROM `categories` ORDER BY RAND() LIMIT 1;"
    # recomendation_genre = execute_query(query_rgt)
    # query_rgc = f"""
    # SELECT shows.show_id, shows.title, shows.rating, shows.description, shows.type
    # FROM shows JOIN showcategories JOIN categories
    # ON shows.show_id = showcategories.show_id AND showcategories.category_id = categories.category_id
    # WHERE categories.category_id = {recomendation_genre[0]['category_id']}
    # ORDER BY RAND() LIMIT 4;
    # """
    # recomendation_content = execute_query(query_rgc)
    #
    # ### RENDER ####
    # content = {"carousel": carousel, "tst": top_selected_type, 'tsc': top_selected_content, "rg": recomendation_genre, "rc": recomendation_content}
    return render_template("home.html")


################################ GENRES GENRES GENRES GENRES GENRES GENRES GENRES GENRES GENRES #######################
@app.route("/api/books")
def api_books():
    query_lg = 'SELECT * FROM books'
    list_books = execute_query(query_lg)
    return jsonify(list_books)

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
