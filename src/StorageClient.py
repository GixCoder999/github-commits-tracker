from pathlib import Path
import json


class StorageClient:
    def __init__(self)->None:
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


    def cleanRepo(self,owner,repo)->None:
        repos = self.load_repos()
        
        if owner in repos and repo in repos[owner]:
            repos[owner].pop(repo)

        with open(self.repos_file,"w") as f:
            json.dump(repos,f)
    

    def cleanAllRepos(self)->None:
        self.repos_file.write_text("{}")


    def showAllRepos(self)->None:
        all_repos = self.load_repos()
       
        if not all_repos:
            print("[gctracker] No Repos Found. Please add some repos first")
            return
        
        print("[gctracker] FORMAT:\nUser / Repo - Last time tracked\n")

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
        all_repos = self.load_unseen()
        
        owners_repo = all_repos.get(owner,{})
        curr_repo = owners_repo.get(repo,{})
        prev_saves:list = curr_repo.get("unseen_commits",[])

        prev_saves.extend(saved_commits)
        
        owners_repo[repo] = {
            "unseen_commits": prev_saves,
            "last_updated": None
        }

        all_repos[owner] = owners_repo

        print(owners_repo)
        with open(self.unseen_file,"w") as file:
            json.dump(all_repos,file)

        return;


    def cleanAllUnseen(self)->None:
        self.unseen_file.write_text("{}")


    def cleanUnseen(self, owner, repo)->None:
        unseens = self.load_unseen()

        if owner in unseens and repo in unseens[owner]:
            unseens[owner][repo]["unseen_commits"] = []
            unseens[owner][repo]["last_updated"] = None

        with open(self.unseen_file, "w") as file:
            json.dump(unseens, file)


    def showUnseenCommits(self)->None:
        unseen = self.load_unseen()
        
        print("[gctracker] FORMAT: OWNER NAME / REPO NAME: UNSEEN COMMIT URL\n")
    
        for owner_name, owner_unseens in unseen.items():
            for repo_name, repo_data in owner_unseens.items():
                
                unseen_shas = repo_data.get("unseen_commits")
                if not unseen_shas:
                    print(f"No Unseen Commits for {owner_name} / {repo_name}")
                    continue

                for commit_sha in unseen_shas:
                    print(f"{owner_name} / {repo_name}: https://github.com/{owner_name}/{repo_name}/commits/{commit_sha}")            


storage = StorageClient()