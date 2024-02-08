import pandas as pd
import re
from FunzioniDB import *


def libri_to_DB(file, connection, righe=None):
    ## CARICA ##
    pd.options.mode.chained_assignment = None
    books_df = pd.read_csv(file, delimiter=";", encoding="latin1", on_bad_lines='skip')[:righe]
    data_books = pd.read_csv(file, delimiter=";", encoding="latin1", on_bad_lines='skip')[:righe]

    books_df.fillna('NULL', inplace=True)
    data_books.fillna('NULL', inplace=True)
    # print(books_df.shape, "Dimensione DB Originale")

    ###PULIZIA###
    # del data_books['image_url']
    # del data_books['small_image_url']

    for i in books_df.index:

        # ## pulizia ISBN ##
        # # OPZIONE 1 SOLO NUMERICI#
        # pat_num = r"^[0-9]+$"
        # if bool(re.fullmatch(pat_num, books_df["ISBN"][i])) is False:
        #     data_books.drop(i, inplace=True)  # Decomentare Se vogliamo solo ISBN numerici
        #     continue
        #     # Sostituzione X sul ISBN e verifica no ripetizione (per avere più dati)
        #     # n = random.randint(0, 9)
        #     # books_df["ISBN"][i] = books_df["ISBN"][i].replace("X", f"{n}").replace("x", f"{n}")
        #     # while books_df["ISBN"].value_counts()[books_df["ISBN"][i]] > 1:
        #     #     books_df["ISBN"][i] = re.sub(r'm$', f"{random.randint(0, 9)}")
        # if len(data_books[data_books["ISBN"] == books_df["ISBN"][i]]) > 1:
        #     print(books_df["ISBN"][i])
        #     # data_books.drop(i, inplace=True)
        #     continue
        #     # Eliminazione di ISBN non numerici
        #     # if bool(re.fullmatch(pat_num, books_df["ISBN"][i])) is False:
        #     #     data_books.drop(i, inplace=True)
        #     #     continue

        # OPZIONE 2 ALFANUMERICI#
        # pat_let = r"^[A-Z0-9]+$"
        # if bool(re.fullmatch(pat_let, books_df["ISBN"][i])) is False:
        #     data.drop(i, inplace=True)

        pat_str = r"^[a-zA-Z0-9.,'?¿()/#&%ñ:;+-_$@! ¡]+$"
        ## PULIZIA TITLE ##
        if bool(re.fullmatch(pat_str, books_df["original_title"][i])) is False or books_df["original_title"][
            i] == "NULL":
            # print(books_df['Book-Title'][i])
            data_books.drop(i, inplace=True)
            continue

        ## PULIZIA AUTHOR ##
        try:
            if bool(re.fullmatch(pat_str, books_df["authors"][i])) is False:
                # print(books_df['Book-Author'][i])
                data_books.drop(i, inplace=True)
                continue
        except:
            if books_df['year'][i] != "NULL":
                data_books.drop(i, inplace=True)
                continue

        ## PULIZIA YEAR ##
        try:
            books_df['year'][i] = int(books_df['year'][i])
        except:
            if books_df['year'][i] != "NULL":
                data_books.drop(i, inplace=True)
                continue

        # ##PULIZIA PUBLISHER##
        # if bool(re.fullmatch(pat_str, books_df['Publisher'][i])) is False:
        #     data_books.drop(i, inplace=True)
        #     continue

        # #PULIZIA IMAGE##
        # if not books_df[''][i].startswith("http://") and not books_df['Image-URL-L'][i].endswith(".jpg"):
        #     data_books.drop(i, inplace=True)
        #     continue

        # if len(list(data_books.columns)) != len(list(data_books.iloc[i])):
        # data_books.drop(i, inplace=True)
        # print(data_books.iloc[i])
        # continue

    # print(data_books.shape, "Dimensione DB Finale")

    #
    # ### DATA IMAGES ###
    # data_books["ISBN_img"] = data_books["ISBN"]
    # data_images = pd.concat([data_books.pop("ISBN_img"), data_books.pop('Image-URL-L')], axis=1)

    ## CONVERTING DF INTO TUPLES ##
    data_books = list(zip(data_books["book_id"],
                          data_books["original_title"],
                          data_books["authors"],
                          data_books["year"],
                          data_books["image_url"],
                          data_books["small_image_url"]))
    # data_images = list(data_images.itertuples(index=False, name=None))

    ## CARICARE I DATI #

    query = f"INSERT INTO books VALUES ({', '.join(list(['%s'] * len(data_books[0])))});"
    execute_many(connection, query, data_books)


