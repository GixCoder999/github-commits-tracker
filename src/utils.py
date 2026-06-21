from tracker import getCommit
from StorageClient import storage


def handleAddRepo(args)->None:
    getCommit(args.owner, args.repo)


def handleShowCommand(args)->None:
    if args.type=="repos":
       storage.showAllRepos()
    elif args.type=="unseen":
        storage.showUnseenCommits()
    

def handleDeleteCommand(args):
    if args.all:
        if args.type=="repos":
            storage.cleanAllRepos()
        elif args.type=="unseen":
            storage.cleanAllUnseen()
    elif args.type=="repos":
        storage.cleanRepo(args.owner,args.repo)
    elif args.type=="unseen":
        storage.cleanUnseen(args.owner,args.repo)


def handleExit(args)->None:
    print("Exiting...")