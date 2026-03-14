from fastapi import APIRouter, HTTPException
from git import Repo, InvalidGitRepositoryError
from pydantic import BaseModel
import os

router = APIRouter()

IGNORE_LIST_FILE = "ignore_list.txt"

def get_ignore_list():
    if os.path.exists(IGNORE_LIST_FILE):
        with open(IGNORE_LIST_FILE) as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

class LocalRepoPath(BaseModel):
    path: str

class IgnoreRepo(BaseModel):
    path: str

@router.post("/scan")
def scan_local_repo(body: LocalRepoPath):
    try:
        if body.path in get_ignore_list():
            return {"ignored": True, "path": body.path}
        repo = Repo(body.path)
        commits = []
        for commit in list(repo.iter_commits())[:20]:
            commits.append({
                "sha": commit.hexsha[:7],
                "message": commit.message.strip(),
                "author": commit.author.name,
                "date": str(commit.authored_datetime),
            })
        return {
            "path": body.path,
            "branch": repo.active_branch.name,
            "commits": commits,
            "is_dirty": repo.is_dirty(),
            "untracked": repo.untracked_files,
        }
    except InvalidGitRepositoryError:
        raise HTTPException(status_code=400, detail="Not a git repository")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ignore")
def add_to_ignore(body: IgnoreRepo):
    with open(IGNORE_LIST_FILE, "a") as f:
        f.write(body.path + "\n")
    return {"ignored": body.path}

@router.get("/ignore")
def get_ignored():
    return {"ignored": get_ignore_list()}

@router.delete("/ignore")
def remove_from_ignore(body: IgnoreRepo):
    ignore = get_ignore_list()
    ignore = [i for i in ignore if i != body.path]
    with open(IGNORE_LIST_FILE, "w") as f:
        f.write("\n".join(ignore))
    return {"removed": body.path, "remaining": ignore}
