import sqlite3
from sqlite3 import Error
from CommandTypes import ArgsType, Arg, Group, BaseCommand


# For testing purposes
# Main is simulating the parser team using the data returned by requests to the interface
def main():
    # parser team makes commands in the form of statements asking about the data
    # db team maps the command to the sql equivalent, runs the query and returns the data to the parser team
    # language is subject to change this is just an example
    interface = Interface(r"IM.db")
    #print("\n".join(["".join(str(x)) for x in interface.select("get highest grossing movie for all directors")]))
    #print("*"*80)
    #print("\n".join(["".join(str(x)) for x in interface.select("get total budget for all directors")]))
    #print("*"*80)
    #print("\n".join(["".join(str(x)) for x in interface.select("get all movies by director", id=3)]))
    #print("*"*80)
    print("\n".join(["".join(str(x)) for x in interface.select("net profit", director="Bong Ho")]))
    interface.close_connection()


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


if __name__ == "__main__":
    main()
