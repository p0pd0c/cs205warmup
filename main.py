from CommandTypes import SQLInterfaceError, InvalidCommandError, DataNotLoadedError
from parser import Parser
from sqlnterface import Interface


def main():
    interface = Interface(r"IM.db")
    parser = Parser(interface)
    user_input = ""
    while user_input != "quit":

        try:
            user_input = parser.get_next_command()
        except DataNotLoadedError:
            print("The data is not loaded. Type command 'load data' then try again")
        except SQLInterfaceError:
            print("Error with SQL interface")
        except InvalidCommandError:
            display_help(self, result)

    interface.close_connection()


if __name__ == "__main__":
    main()
