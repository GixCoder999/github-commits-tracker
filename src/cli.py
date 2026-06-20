import argparse as ag
from utils import handleAddRepo,handleShowCommand,handleExit

def main():
    parser = ag.ArgumentParser(prog="gctrack",description="This is a github commits tracking tool")
    subparser = parser.add_subparsers(
        dest="command",
        required=True
    )

    track_parser = subparser.add_parser("add")
    track_parser.add_argument("owner")
    track_parser.add_argument("repo")

    show_parser = subparser.add_parser("show")
    show_parser.add_argument("type",choices=["repos","unseen"])

    exit_parser = subparser.add_parser("exit")
    exit_parser.add_argument("--force")

    args = parser.parse_args()

    COMMANDS = {
        "add": handleAddRepo,
        "show": handleShowCommand,
        "exit": handleExit
    }

    COMMANDS[args.command](args);

if __name__=="__main__":
    main()