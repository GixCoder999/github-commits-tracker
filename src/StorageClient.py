from pathlib import Path
import json

padding = "\t\t"

class StorageClient:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.data_dir = self.base_dir / "data"

        self.repos_file = self.data_dir / "repos.json"
        self.unseen_file = self.data_dir / "unseen_commits.json"

        #init dirs and files
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.repos_file.exists():
            self.repos_file.write_text(json.dumps({}))
        
        if not self.unseen_file.exists():
            self.unseen_file.write_text(json.dumps({}))

    def load_repos(self)->dict:
        if not self.repos_file.exists():
            return {}
        
        try:
            with open(self.repos_file,"r") as f:
                repos = json.load(f)
        except json.JSONDecodeError:
            repos = {}
        return repos
    

    def setRepo(self,owner,repo,sha)->None:
        repos = storage.load_repos()
        owners_repos = repos.get(owner, {})

        owners_repos[repo] = {
            "latest_sha": sha,
            "last_checked": None
        }

        # ensure the owner's entry is stored back into the top-level dict
        repos[owner] = owners_repos

        with open(self.repos_file, "w") as file:
            json.dump(repos, file)


    def showAllRepos(self)->None:
        all_repos = self.load_repos()
       
        if not all_repos:
            print("[gctracker] No Repos Found. Please add some repos first")
            return
        
        print("[gctracker] FORMAT:\nUser / Repo - Last time tracked")

        for owner,owners_repos in all_repos.items():
            for repo_name,repo_data in owners_repos.items():
                print(f"{owner} / {repo_name} - {repo_data.get("last_checked")}\n")


    def load_unseen(self)->dict:
        if not self.unseen_file.exists():
            return {}
        
        with open(self.unseen_file,"r") as f:
            unseen = json.load(f)
        
        return unseen


    def saveUnseenCommits(self,owner,repo,saved_commits)->None:
        with open(self.unseen_file,"r") as file:
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
        with open(self.unseen_file,"w") as file:
            json.dump(owners_repo,file)

        return;


    def showUnseenCommits(self):
        print("Showing Unseen Commits...\n")

storage = StorageClient()