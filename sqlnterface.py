import sqlite3
from sqlite3 import Error
from CommandTypes import ArgsType, Arg, Group, BaseCommand


class Interface:
    DEBUG = False
    conn = None

    def __init__(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
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
        print(command, kwargs)
        sql = None

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
                print("The kwargs name: ", kwargs["name"])
                curr.execute(sql, [kwargs["name"]])
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
                    order by sum(gross) desc
                """
                curr = self.conn.cursor()
                curr.execute(sql)
                return curr.fetchall()
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
