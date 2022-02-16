import shlex
from CommandTypes import ArgsType, Arg, Group, BaseCommand
from sqlnterface import Interface


class Parser:
    def __init__(self, sql_interface: Interface):
        self.commands = [
            BaseCommand("net", [Group(["budget", "profit"]), Group(["director", "movie"])], [Arg(ArgsType.Name, True)]),

            BaseCommand("how many made by", [], [Arg(ArgsType.Name, True)]),
            BaseCommand("how many", [Group(["directors", "movies"])], []),

            BaseCommand("which movies by", [], [Arg(ArgsType.Name, True)]),

            BaseCommand("oldest", [Group(["movie", "director"])], []),
            BaseCommand("newest", [Group(["movie", "director"])], []),

            BaseCommand("movies", [Group(["after", "before"])], [Arg(ArgsType.Date, True)]),

            BaseCommand("budget", [], [Arg(ArgsType.Name, True)]),

            BaseCommand("most successful", [Group(["movie", "director"])], []),
            BaseCommand("least successful", [Group(["movie", "director"])], []),

            BaseCommand("load data", [], [])
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
                print("Shlex Parse: ", shlex.split(raw_command[len(base_command.command) + 1: len(raw_command)]))
                words = shlex.split(raw_command[len(base_command.command) + 1: len(raw_command)])

                print("Words: ", words)

                # Returns None if command does not have enough arguments and keywords
                if len(words) < len(base_command.groups) + len(base_command.args):
                    print("Incorrect Command")
                    return None

                # Creates boolean array to check keywork positions
                correct_groups = [False] * len(base_command.groups)
                for i in range(len(base_command.groups)):
                    # Group of correct keywords
                    group = base_command.groups[i]

                    for keyword in group.keywords:
                        if words[i] == keyword:
                            print("Found keyword:", keyword)

                            # Adds keyword to command_data to send to sql_interface
                            command_data["keywords"].append(keyword)

                            # Sets to true if keyword is in correct position in command
                            correct_groups[i] = True

                # Remove keywords from array, to make it easier to parse multiple arguments
                words = words[len(base_command.groups):]
                print(words)

                # Checks all arguments are in the correct order
                if not (correct_groups == [True] * len(base_command.groups)):
                    print("Incorrect Command")
                    return None

                print("Valid Command...")

                # Parse all arguments using their type given in BaseCommands
                for index, arg in enumerate(base_command.args):
                    command_data[arg.type.value] = words[index]

            if valid_command:

                # Specific case for load data command
                if intended_command.command == "load data":
                    return self.sql_interface.load_data()

                # Stop after first valid command, since some base commands share words with
                # others so order is important.
                print("Command sent to sql with data: ", command_data)
                return self.sql_interface.select(intended_command, **command_data)

        # No valid command found to match with raw command
        return None

    def get_next_command(self):
        # Get raw input
        raw_input = input("> ")

        if raw_input == "quit":
            return "quit"

        result = self.process_command(raw_input)
        if result is not None:
            # prints result from sql interface
            print(result)

        else:
            # Displays help message
            print("The command you entered was invalid...")
            print("The following are valid base commands: ")

            slash = " / "
            quote = '"'
            for cmd in self.commands:
                groups = cmd.groups
                args = cmd.args

                # Bit of mess but, in one line :), f strings are cool
                print(f'{cmd.command} {" ".join(f"[ {slash.join(group.keywords)} ]" for group in groups)} {" ".join(f"{quote}{arg.type.value}{quote}" for arg in args)}')
