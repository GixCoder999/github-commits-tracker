from StorageClient import storage
import requests


def handleGithubFetchError(response):
    if response.status_code != 200:
        raise Exception(f"GitHub API Error: {response.json().get('message')}")


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
        
        while(True):
            choice = input("Mark as seen? [Y/n], Select No for saving commit to json: ")
            if choice.isalpha() and (choice.lower()=='y' or choice.lower()=="n"):
                break
            print("[ERROR] Please Enter 'Y'/'y' for YES and 'N'/'n' for No")

        if choice.lower()=="y":
            continue
        
        #save to json
        print(f"\n[SAVING COMMIT] {owner}/{repo}")
        saved_commits.append(commit)
        print(f"Commit saved to unseen_commits.json\n")

    return saved_commits;


def getCommit(owner, repo)->None:
    if isCheckingFirstTime(owner,repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=1"
        response = requests.get(url)
        
        handleGithubFetchError(response)

        repos = response.json()

        commit = repos[0]
        latest_sha = commit["sha"]
        storage.setRepo(owner,repo,latest_sha)
        
        return;

    #in case of not first time
    last_sha = storage.load_repos()[owner][repo]["latest_sha"]
    commits_shas,latestCommitSha = getNewCommits(owner,repo,last_sha);
    
    storage.setRepo(owner,repo,latestCommitSha) #update latest sha
    saved_commits = logNewCommits(commits_shas, owner, repo) #Logs New Commits into a json file as unseen
    storage.saveUnseenCommits(owner,repo,saved_commits)


def isCheckingFirstTime(owner,repo)->bool:
    all_repos = storage.load_repos();
    owners_repos = all_repos.get(owner,{})
 
    if repo not in owners_repos:
        return True

    return False
