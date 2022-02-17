import shlex
from CommandTypes import ArgsType, Arg, Group, BaseCommand, SQLInterfaceError, DataNotLoadedError, InvalidCommandError
from sqlnterface import Interface


class Parser:
    def __init__(self, sql_interface: Interface):
        self.commands = [
            BaseCommand("net", [Group(["budget", "profit"]), Group(["director", "movie"])], [Arg(ArgsType.Name, True)]),

            BaseCommand("get", [Group(["movies", "directors"])], []),

            BaseCommand("how many made by", [], [Arg(ArgsType.Name, True)]),
            BaseCommand("how many", [Group(["directors", "movies"])], []),

            BaseCommand("which movies by", [], [Arg(ArgsType.Name, True)]),

            BaseCommand("oldest", [Group(["movie", "director"])], []),
            BaseCommand("newest", [Group(["movie", "director"])], []),

            BaseCommand("movies", [Group(["after", "before"])], [Arg(ArgsType.Date, True)]),

            BaseCommand("budget", [], [Arg(ArgsType.Name, True)]),

            BaseCommand("most successful", [Group(["movie", "director"])], []),
            BaseCommand("least successful", [Group(["movie", "director"])], []),

            BaseCommand("load data", [], []),
            BaseCommand("toggle debug", [], [])
        ]

        self.sql_interface = sql_interface

    def process_command(self, raw_command):
        valid_command = False
        intended_command = None
        command_data = {"keywords": []}

        # Loop through all commands created
        for base_command in self.commands:

            # Match command with base command structure
            if raw_command.startswith(base_command.command):
                valid_command = True
                intended_command = base_command

                # Shlex debug
                self.sql_interface.DEBUG and print("Shlex Parse: ", shlex.split(raw_command[len(base_command.command) + 1: len(raw_command)]))

                words = shlex.split(raw_command[len(base_command.command) + 1: len(raw_command)])

                # Words debug
                self.sql_interface.DEBUG and print("Words: ", words)

                # Returns None if command does not have enough arguments and keywords
                if len(words) < len(base_command.groups) + len(base_command.args):
                    raise InvalidCommandError("Incorrect Command")

                # Creates boolean array to check keywork positions
                correct_groups = [False] * len(base_command.groups)
                for i in range(len(base_command.groups)):
                    # Group of correct keywords
                    group = base_command.groups[i]

                    for keyword in group.keywords:
                        if words[i] == keyword:
                            # keyword debug
                            self.sql_interface.DEBUG and print("Found keyword:", keyword)

                            # Adds keyword to command_data to send to sql_interface
                            command_data["keywords"].append(keyword)

                            # Sets to true if keyword is in correct position in command
                            correct_groups[i] = True

                # Remove keywords from array, to make it easier to parse multiple arguments
                words = words[len(base_command.groups):]

                # Checks all arguments are in the correct order
                if not (correct_groups == [True] * len(base_command.groups)):
                    raise InvalidCommandError("Incorrect argument order")

                # Display valid command debug
                self.sql_interface.DEBUG and print("Valid Command...")

                # Parse all arguments using their type given in BaseCommands
                for index, arg in enumerate(base_command.args):
                    command_data[arg.type.value] = words[index]

            if valid_command:

                # Specific case for load data command
                if intended_command.command == "load data":
                    if self.sql_interface.load_data():
                        return "Data has been loaded!", base_command
                    else:
                        return "Data is already loaded!", base_command

                if self.sql_interface.data_loaded:
                    # Stop after first valid command, since some base commands share words with
                    # others so order is important.
                    self.sql_interface.DEBUG and print("Command sent to sql with data: ", command_data)
                    return self.sql_interface.select(intended_command, **command_data), base_command

                else:
                    # Raise exception to be caught by main
                    raise DataNotLoadedError("Data must be loaded first!")

        # No valid command found to match with raw command
        raise InvalidCommandError("No command found")

    def pretty_print(self, result, base_command):
        # add special case for load data since returns a simple string
        print(result)
        # print("from command: ", base_command)
        if base_command.command == "net":
            print("$", result[0][0],sep="")

        if base_command.command == "get":
            for x in result:
                for y in x:
                    print(y)

        if base_command.command == "how many made by":
            print(result[0][0])

        if base_command.command == "how many":
            print(result[0][0])

        if base_command.command == "which movies by":
            for x in result:
                for y in x:
                    print(y)

        if base_command.command == "oldest":
            for x in result:
                for y in x:
                    print(y)

        if base_command.command == "newest":
            for x in result:
                for y in x:
                    print(y)

        if base_command.command == "movies":
            for x in result:
                for y in x:
                    print(y)

        if base_command.command == "budget":
            print("$",result[0][0],sep="")

        if base_command.command == "most successful":
            print(result[0][0])

        if base_command.command == "least successful":
            print(result[0][0])


    def display_help(self):
        print("The command you entered was invalid...")
        print("The following are valid base commands: ")

        slash = " / "
        quote = '"'
        for cmd in self.commands:
            groups = cmd.groups
            args = cmd.args

            # Bit of mess but, in one line :), f strings are cool
            print(f'{cmd.command} {" ".join(f"[ {slash.join(group.keywords)} ]" for group in groups)} {" ".join(f"{quote}{arg.type.value}{quote}" for arg in args)}')

    def get_next_command(self):
        # Get raw input
        raw_input = input("> ")

        if raw_input == "quit":
            # Return quit to exit in main
            return "quit"

        # gets result from sql interface
        result, base_command = self.process_command(raw_input)
        if result is not None:
            # prints result from sql interface
            self.pretty_print(result, base_command)

        else:
            raise SQLInterfaceError

