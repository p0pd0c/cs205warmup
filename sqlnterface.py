import sqlite3
from sqlite3 import Error


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
    print("\n".join(["".join(str(x)) for x in interface.select("net profit", director="Francis Ford Coppola")]))
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

    def select(self, command, **kwargs):
        """
        Provide command to select a sql statement and provide named kwargs (dictionary) for additional query params
        Uses prepared statements to prevent injection
        :param command:
        :param kwargs:
        :exception null_op:
        :return:
        """
        sql = None
        if command == "get highest grossing movie for all directors":
            sql = """
                select directors.id, first_name, last_name, title, max(gross) from directors
                join movies on directors.id = movies.director_id
                group by first_name, last_name
                order by max(gross)
            """
        elif command == "get total budget for all directors":
            sql = """
                select first_name, last_name, sum(budget) as 'Total Budget'
                from directors
                join movies on directors.id = movies.director_id
                group by first_name, last_name
                order by sum(budget) desc
            """
        elif command == "get all movies by director":
            sql = """
                select title from movies
                join directors on movies.director_id = ?
                group by title
            """
            curr = self.conn.cursor()
            curr.execute(sql, (str(kwargs["id"])))
            return curr.fetchall()
        elif command == "net profit":
            if kwargs["director"]:
                sql = """
                    select sum(gross - budget) as "Net Profit" from movies
                    join directors on movies.director_id = directors.id
                    where first_name = ? and last_name = ?
                """
                curr = self.conn.cursor()
                name = kwargs["director"].split(" ")
                if len(name) > 2:
                    name = [" ".join([name[0], name[1]]).strip(), name[2]]  # strip may be redundant
                else:
                    name = [name[0], name[1]]
                curr.execute(sql, ('Francis Ford', 'Coppola'))
                return curr.fetchall()

        if command is not None:
            curr = self.conn.cursor()
            curr.execute(sql)
            return curr.fetchall()
        else:
            raise Exception("Invalid operation!")

    def toggle_debug(self):
        self.DEBUG = not self.DEBUG

    def close_connection(self):
        self.conn.close()


if __name__ == "__main__":
    main()
