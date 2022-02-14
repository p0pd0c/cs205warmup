from parser import Parser
from sqlnterface import Interface


def main():
    interface = Interface(r"IM.db")
    parser = Parser(interface)
    user_input = ""
    while user_input != "quit":
        user_input = parser.get_next_command()
    interface.close_connection()


if __name__ == "__main__":
    main()
