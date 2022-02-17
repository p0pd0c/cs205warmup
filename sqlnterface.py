import csv
import sqlite3
from sqlite3 import Error
from CommandTypes import BaseCommand


class Interface:
    DEBUG = False
    conn = None
    data_loaded = False

    def __init__(self, db_file):
        try:
            # create connection to the database, store it in the instance
            self.conn = sqlite3.connect(db_file)

            # check if the tables exist, otherwise data is not loaded
            curr = self.conn.cursor()
            # we do this by checking the master table for any tables that are not prepended with sqlite_
            # we know the data is loaded if the tables exist
            curr.execute("""
                select count(name) from sqlite_schema 
                where type in ('table') and name not like 'sqlite_%';
            """)
            num_tables = curr.fetchall()[0][0]
            self.DEBUG and print("Number of tables: ", num_tables)
            if num_tables == 2:
                self.DEBUG and print("Tables detected")
                self.data_loaded = True
            else:
                self.DEBUG and print("Tables not detected")
            if self.DEBUG:
                print(sqlite3.version)
        except Error as e:
            print(e)

    def select(self, command: BaseCommand, **kwargs):
        """
        Provide command to select a sql statement and provide named kwargs (dictionary) for additional query params
        Uses prepared statements to prevent injection
        :param command:
        :param kwargs:
        :exception null_op:
        :return:
        """
        self.DEBUG and print(command, kwargs)
        sql = None
        if command.command == "toggle debug":
            self.DEBUG = not self.DEBUG
            return []
        if command.command == "net":
            if kwargs["keywords"][1] == "director":
                if kwargs["keywords"][0] == "profit":
                    sql = """
                        select sum(gross - budget) as "Net Profit" from movies
                        join directors on movies.director_id = directors.id
                        where first_name = ? and last_name = ?
                    """
                elif kwargs["keywords"][0] == "budget":
                    sql = """
                        select first_name, last_name, sum(budget) as 'Total Budget'
                        from directors
                        join movies on directors.id = movies.director_id
                        where first_name = ? and last_name = ?
                    """
                curr = self.conn.cursor()
                name = self.split_name(kwargs["name"])
                curr.execute(sql, (name[0], name[1]))
                return curr.fetchall()
            elif kwargs["keywords"][1] == "movie":
                if kwargs["keywords"][0] == "profit":
                    sql = """
                        select sum(gross - budget) as "Net Profit" from movies
                        where title = ?
                    """
                elif kwargs["keywords"][0] == "budget":
                    sql = """
                        select budget from movies
                        where title = ?
                    """
                curr = self.conn.cursor()
                self.DEBUG and print("The kwargs name: ", kwargs["name"])
                curr.execute(sql, [kwargs["name"]])
                return curr.fetchall()
        elif command.command == "get":
            if kwargs["keywords"][0] == "movies":
                sql = """
                    select title from movies
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return curr.fetchall()
            elif kwargs["keywords"][0] == "directors":
                sql = """
                    select first_name, last_name from directors
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return curr.fetchall()
        elif command.command == "how many made by":
            sql = """
                select count(title) from movies
                join directors on movies.director_id = directors.id
                where first_name = ? and last_name = ?
            """
            curr = self.conn.cursor()
            name = self.split_name(kwargs["name"])
            curr.execute(sql, [name[0], name[1]])
            return curr.fetchall()
        elif command.command == "how many":
            if kwargs["keywords"][0] == "directors":
                sql = """
                    select count(first_name) from directors
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return curr.fetchall()
            elif kwargs["keywords"][0] == "movies":
                sql = """
                    select count(title) from movies
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return curr.fetchall()
        elif command.command == "which movies by":
            sql = """
                select title from movies 
                join directors on movies.director_id = movies.id
                where first_name = ? and last_name = ?
            """
            curr = self.conn.cursor()
            name = self.split_name(kwargs["name"])
            curr.execute(sql, [name[0], name[1]])
            return curr.fetchall()
        elif command.command == "oldest":
            if kwargs["keywords"][0] == "director":
                sql = """
                    select first_name, last_name from directors
                    order by age desc
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return [curr.fetchall()[0]]
            elif kwargs["keywords"][0] == "movie":
                sql = """
                    select title from movies
                    order by year asc
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return [curr.fetchall()[0]]
        elif command.command == "newest":
            if kwargs["keywords"][0] == "director":
                sql = """
                    select first_name, last_name from directors
                    order by age asc
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return [curr.fetchall()[0]]
            if kwargs["keywords"][0] == "movie":
                sql = """
                    select title from movies
                    order by year desc
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return [curr.fetchall()[0]]
        elif command.command == "movies":
            if kwargs["keywords"][0] == "before":
                sql = """
                    select title from movies 
                    where year < ?
                """
                curr = self.conn.cursor()
                curr.execute(sql, [kwargs["date"]])
                return curr.fetchall()
            elif kwargs["keywords"][0] == "after":
                sql = """
                    select title from movies
                    where year > ?
                """
                curr = self.conn.cursor()
                curr.execute(sql, [kwargs["date"]])
                return curr.fetchall()
        elif command.command == "budget":
            sql = """
                select budget from movies
                where title = ?
            """
            curr = self.conn.cursor()
            curr.execute(sql, [kwargs["name"]])
            return curr.fetchall()
        elif command.command == "most successful":
            if kwargs["keywords"][0] == "movie":
                sql = """
                    select title, max(gross) from movies
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return curr.fetchall()
            elif kwargs["keywords"][0] == "director":
                sql = """
                    select first_name, last_name, sum(gross) from movies
                    join directors on movies.director_id = directors.id
                    group by first_name, last_name
                    order by sum(gross) desc
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return [curr.fetchall()[0]]
        elif command.command == "least successful":
            if kwargs["keywords"][0] == "movie":
                sql = """
                    select title, min(gross) from movies
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return curr.fetchall()
            elif kwargs["keywords"][0] == "director":
                sql = """
                    select first_name, last_name, sum(gross) from movies
                    join directors on movies.director_id = directors.id
                    group by first_name, last_name
                    order by sum(gross) asc
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return [curr.fetchall()[0]]
        return None

    def split_name(self, inpt):
        name = inpt.split(" ")
        if len(name) > 2:
            name = [" ".join([name[0], name[1]]).strip(), name[2]]
        elif len(name) == 2:
            name = [name[0], name[1]]
        else:
            name = name[0]
        return name

    def toggle_debug(self):
        self.DEBUG = not self.DEBUG

    def close_connection(self):
        self.conn.close()

    def load_data(self):
        self.DEBUG and print("Data loaded: ", self.data_loaded)
        if not self.data_loaded:
            curr = self.conn.cursor()
            curr.executescript("""
                CREATE TABLE movies(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    title CHAR(32) NOT NULL,
                    gross LONG INTEGER NOT NULL,
                    budget LONG INTEGER NOT NULL,
                    director_id INTEGER,
                    FOREIGN KEY(director_id) REFERENCES directors(id)
                );
    
                CREATE TABLE directors(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name CHAR(32) NOT NULL,
                    last_name CHAR(32) NOT NULL,
                    movies_made INTEGER NOT NULL, age INTEGER NOT NULL
                );
            """)
            with open("CS205_Warmup_Project_Data-movies.csv", newline="") as movies_file:
                movies_reader = csv.reader(movies_file, delimiter=",")
                movies_reader = list(movies_reader)
                curr.executemany("""
                                    INSERT INTO movies VALUES(?,?,?,?,?,?)
                                """, movies_reader[1:])
                movies_file.close()
                self.DEBUG and print("Loaded data from movies file")
            with open("CS205_Warmup_Project_Data-directors.csv", newline="") as directors_file:
                directors_reader = csv.reader(directors_file, delimiter=",")
                directors_reader = list(directors_reader)
                curr.executemany("""
                                    INSERT INTO directors VALUES(?,?,?,?,?)
                                """, directors_reader[1:])
                directors_file.close()
                self.DEBUG and print("Loaded data from directors file")
            self.conn.commit()
            self.data_loaded = True
            return True
        else:
            return False
