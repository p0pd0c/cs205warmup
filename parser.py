import enum
from dataclasses import dataclass
from enum import Enum
import shlex

class ArgsType(Enum):
    Date = 1
    Name = 2


@dataclass
class Arg:
    type: ArgsType
    required: bool


@dataclass
class Group:
    keywords: list[str]


@dataclass
class BaseCommand:
    command: str
    groups: list[Group]
    # hasArg: bool
    args: list[Arg]


class Parser:

    def __init__(self, sql_interface):

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

    def get_next_command(self):
        raw_input = input("> ")

    def process_command(self, raw_command):

        for base_command in self.commands:

            if raw_command.startswith(base_command.command):

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
                        pass

                return


# Parser(None).process_command('net budget movie "The Shawshank Redemption"')
# Parser(None).process_command('how many directors')
# Parser(None).process_command('how many made by "Christopher Nolan"')
Parser(None).process_command('movies after "June 10 2010"')