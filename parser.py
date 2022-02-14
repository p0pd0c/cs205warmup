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
        ]

        self.sql_interface = sql_interface

    def process_command(self, raw_command):
        valid_command = False
        intended_command = None
        command_data = {"keywords": []}
        for base_command in self.commands:
            if raw_command.startswith(base_command.command):
                valid_command = True
                intended_command = base_command
                print(shlex.split(raw_command[len(base_command.command) + 1: len(raw_command)]))
                words = shlex.split(raw_command[len(base_command.command) + 1: len(raw_command)])
                # raw_command[len(base_command.command) + 1: len(raw_command)].split(' ')
                if len(words) < len(base_command.groups) + len(base_command.args):
                    print("Incorrect Command")
                    return

                correct_groups = [False] * len(base_command.groups)
                for i in range(len(base_command.groups)):
                    group = base_command.groups[i]
                    for keyword in group.keywords:
                        if words[i] == keyword:
                            print("Found keyword:", keyword)
                            command_data["keywords"].append(keyword)
                            correct_groups[i] = True

                if not (correct_groups == [True] * len(base_command.groups)):
                    print("Incorrect Command")
                    return

                print("Valid Command...")
                for arg in base_command.args:
                    if arg.type == ArgsType.Date:
                        # parse date
                        print("Parse Date...")
                        pass
                    elif arg.type == ArgsType.Name:
                        # parse director and movie name
                        print("Parse Name...")
                        command_data["name"] = "Christopher Nolan"
                        pass
        if valid_command:
            return self.sql_interface.select(intended_command, **command_data)
        else:
            print("The command you entered was invalid...")
            print("The following are valid base commands: ")
            for cmd in self.commands:
                print(cmd.command)

    def get_next_command(self):
        raw_input = input("> ")
        if raw_input == "quit":
            return "quit"

        result = self.process_command(raw_input)
        if result is not None:
            print(result)


def main():
    interface = Interface("IM.db")
    Parser(interface).process_command('net budget movie "The Shawshank Redemption"')
    Parser(interface).process_command('how many directors')
    Parser(interface).process_command('how many made by "Christopher Nolan"')
    Parser(interface).process_command('movies after "June 10 2010"')


if __name__ == "__main__":
    main()
