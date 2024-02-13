from datetime import datetime
import pandas as pd
import re
from FunzioniDB import *


def prestiti_to_DB(file, connection, righe=None):
    ## CARICA ##
    pd.options.mode.chained_assignment = None
    loan_df = pd.read_csv(file, delimiter=";", encoding="latin1", on_bad_lines='skip')[:righe]
    data_loan = pd.read_csv(file, delimiter=";", encoding="latin1", on_bad_lines='skip')[:righe]
    loan_df.fillna('NULL', inplace=True)
    data_loan.fillna('NULL', inplace=True)

    for i in loan_df.index:
        pat_str = r"^[a-zA-Z0-9.,'?¿()/#&%ñ:;+-_$@! ¡]+$"

        ## PULIZIA ANNO ##
        date_obj = datetime.strptime(loan_df["date of loan"][i], "%d-%m-%Y")
        data_loan["date of loan"][i] = date_obj.strftime("%Y-%m-%d")

    ## CONVERTING DF INTO TUPLES ##
    data_users = list(zip(data_loan["id loan"],
                          data_loan["id book"],
                          data_loan["id user"],
                          data_loan["date of loan"]))

    ##CARICA DATI ##
    query = f"INSERT INTO loan VALUES ({', '.join(list(['%s'] * len(data_users[0])))});"
    execute_many(connection, query, data_users)

