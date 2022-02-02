import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    Create connection to sqlite db from db file
    :param db_file:
    :return sqlite connection | None:
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        return conn


def insert_movie(conn, movie):
    """
    Insert a movie record
    :param conn:
    :param movie:
    :return id of the movie:
    """

    sql = '''
        insert into movies(year, title, gross, budget, director_id)
        values (?,?,?,?,?)
    '''

    curr = conn.cursor()
    curr.execute(sql, movie)
    conn.commit()
    return curr.lastrowid


def insert_director(conn, director):
    sql = '''
            insert into directors(first_name, last_name, movies_made, age)
            values (?,?,?,?)
        '''

    curr = conn.cursor()
    curr.execute(sql, director)
    conn.commit()
    return curr.lastrowid


def main():
    conn = create_connection(r"IM.db")

    movie = (2022, "New Movie", 1000000, 10000, 1)
    movie_id = insert_movie(conn, movie)
    print("New movie id:", movie_id)

    director = ("Jared", "DiScipio", 5, 20)
    director_id = insert_director(conn, director)
    print("New director id:", director_id)

    conn.close()


if __name__ == "__main__":
    main()
