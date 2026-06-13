import requests
import json

path = "./data"
def initialize()->dict:
    with open(f"{path}/repos.json", "r") as f:
        repos = json.load(f)
    return repos


def setRepo(owner,repo,sha)->None:
    repos = initialize()
    owners_repos = repos.get(owner, {})

    owners_repos[repo] = {
        "latest_sha": sha,
        "last_checked": None
    }

    # ensure the owner's entry is stored back into the top-level dict
    repos[owner] = owners_repos

    with open(f"{path}/repos.json", "w") as file:
        json.dump(repos, file)


def saveUnseenCommits(owner,repo,saved_commits)->None:
    with open(f"{path}/unseen_commits.json","r") as file:
        all_repos = json.load(file)
    
    owners_repo = all_repos.get(owner,{})
    curr_repo = owners_repo.get(repo,{})
    prev_saves:list = curr_repo.get("unseen_commits",[])

    prev_saves.extend(saved_commits)
    
    owners_repo[repo] = {
        "unseen_commits": prev_saves,
        "last_updated": None
    }
    print(owners_repo)
    with open(f"{path}/unseen_commits.json","w") as file:
        json.dump(owners_repo,file)

    return;


def getNewCommits(owner,repo,last_sha)->tuple:
    #do something to get new commits
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(url)
    commits = response.json()

    commits_shas = []
    for commit in commits:
        current_sha = commit["sha"]
        
        if current_sha==last_sha:
            break

        commits_shas.append(current_sha)
        
    new_latest_commit_sha = commits_shas[0] if commits_shas else last_sha
    return commits_shas,new_latest_commit_sha;



def logNewCommits(commits_sha, owner, repo)->list:
    saved_commits = []
    for commit in commits_sha:
        url = f"https://github.com/{owner}/{repo}/commit/{commit}"
        print(f"[NEW COMMIT] {owner}/{repo}")
        print(f"\tSHA: {commit}\n\tURL: {url}")
        
        choice = input("Mark as seen? [Y/n], Select No for saving commit to json: ")
        if choice.isalpha() and choice.lower()=="y":
            continue;
    
        #save to json
        print(f"\n[SAVING COMMIT] {owner}/{repo}")
        saved_commits.append(commit)
        print(f"Commit saved to unseen_commits.json\n")

    return saved_commits;


def getCommit(owner, repo)->None:
    if isCheckingFirstTime(owner,repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=1"
        response = requests.get(url)
        repos = response.json()

        commit = repos[0]
        latest_sha = commit["sha"]
        setRepo(owner,repo,latest_sha)
        
        return;


    last_sha = initialize()[owner][repo]["latest_sha"]
    commits_shas,latestCommitSha = getNewCommits(owner,repo,last_sha);
    
    setRepo(owner,repo,latestCommitSha) #update latest sha
    saved_commits = logNewCommits(commits_shas, owner, repo) #Logs New Commits into a json file as unseen
    saveUnseenCommits(owner,repo,saved_commits)


def isCheckingFirstTime(owner,repo)->bool:
    all_repos = initialize();
    owners_repos = all_repos.get(owner)
 
    if not owners_repos:
        return True

    print(owners_repos)

    # if the specific repo isn't present, it's the first time checking it
    if repo not in owners_repos:
        return True

    return False



getCommit("GixCoder999","SoftLib")