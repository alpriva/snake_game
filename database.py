import psycopg2


def add_user(name, score):

    con = psycopg2.connect(database="Snake_game_db", user="postgres", password="13091988", host="localhost", port="5432")
    print("Database opened successfully")
    con.autocommit = True
    cursor = con.cursor()
    cursor.execute("INSERT INTO users VALUES (%s, %s)", (name, score))
    con.commit()
    print("Records inserted")
    # Closing the connection
    con.close()





