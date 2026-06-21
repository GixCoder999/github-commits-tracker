import argparse as ag
from utils import handleAddRepo,handleShowCommand,handleDeleteCommand,handleExit

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

    delete_parser = subparser.add_parser("delete")
    delete_parser.add_argument("type",choices=["repos","unseen"])
    delete_parser.add_argument("owner",nargs="?")
    delete_parser.add_argument("repo",nargs="?")
    delete_parser.add_argument("--all",action="store_true")

    exit_parser = subparser.add_parser("exit")
    exit_parser.add_argument("--force")

    args = parser.parse_args()

    COMMANDS = {
        "add": handleAddRepo,
        "show": handleShowCommand,
        "delete": handleDeleteCommand,
        "exit": handleExit
    }

    COMMANDS[args.command](args);

if __name__=="__main__":
    main()