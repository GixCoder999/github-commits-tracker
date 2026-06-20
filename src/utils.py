from tracker import getCommit
from StorageClient import storage

def handleAddRepo(args)->None:
    getCommit(args.owner, args.repo)


def handleShowCommand(args)->None:
    if args.type=="repos":
       storage.showAllRepos()
    elif args.type=="unseen":
        storage.showUnseenCommits()
    

def handleExit(args)->None:
    print("Exiting...")