from CommandTypes import SQLInterfaceError, InvalidCommandError, DataNotLoadedError
from parser import Parser
from sqlnterface import Interface


def main():
    # Create instance of SQL interface to be passed into parser to send commands
    interface = Interface(r"IM.db")

    # Create parser instance to interact with input
    parser = Parser(interface)

    # Loop until user is done
    user_input = ""
    while user_input != "quit":

        try:
            # Gets next command to send to the sql interface
            user_input = parser.get_next_command()

        except DataNotLoadedError:
            # Catches errors related to the data not being loaded, so no database file has been found
            print("The data is not loaded. Type command 'load data' then try again")

        except SQLInterfaceError:
            # This error should not appear during the execution of the program since all commands
            # sent to the sql interface should return something
            print("Error with SQL interface")

        except InvalidCommandError:
            # This exception is caused by the parser not being able to recognize the command
            # or has not enough arguments, so prints help message showing all commands
            parser.display_help()

    # Close connection when user is done
    interface.close_connection()


if __name__ == "__main__":
    main()
