from datetime import datetime
import pandas as pd
import re
from FunzioniDB import *


def utenti_to_DB(file, connection, righe=None):
    ## CARICA ##
    pd.options.mode.chained_assignment = None
    users_df = pd.read_csv(file, delimiter=";", encoding="latin1", on_bad_lines='skip')[:righe]
    data_users = pd.read_csv(file, delimiter=";", encoding="latin1", on_bad_lines='skip')[:righe]
    users_df.fillna('NULL', inplace=True)
    data_users.fillna('NULL', inplace=True)

    for i in users_df.index:
        pat_str = r"^[a-zA-Z0-9.,'?¿()/#&%ñ:;+-_$@! ¡]+$"
        ## PULIZIA MEMBER NAME ##
        if bool(re.fullmatch(pat_str, users_df["Member Name"][i])) is False or users_df["Member Name"][i] == "NULL":
            # print(books_df['Book-Title'][i])
            data_users.drop(i, inplace=True)
            continue

        ## PULIZIA ANNO ##
        date_obj = datetime.strptime(users_df["Date of Birth"][i], "%d-%m-%Y")
        data_users["Date of Birth"][i] = date_obj.strftime("%Y-%m-%d")

    ## CONVERTING DF INTO TUPLES ##
    data_users = list(zip(data_users["Id"],
                          data_users["Member Name"],
                          data_users["Date of Birth"]))

    ##CARICA DATI ##

    query = f"INSERT INTO users VALUES ({', '.join(list(['%s'] * len(data_users[0])))});"
    execute_many(connection, query, data_users)



