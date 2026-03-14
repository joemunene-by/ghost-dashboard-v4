from fastapi import APIRouter, HTTPException
from github import Github
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()
g = Github(os.getenv("GITHUB_TOKEN"))

@router.get("/")
def get_all_repos():
    try:
        user = g.get_user()
        repos = []
        for repo in user.get_repos():
            repos.append({
                "name": repo.name,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language,
                "private": repo.private,
                "url": repo.html_url,
                "updated_at": str(repo.updated_at),
                "size": repo.size,
                "open_issues": repo.open_issues_count,
                "default_branch": repo.default_branch,
            })
        return {"repos": repos, "total": len(repos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{repo_name}/commits")
def get_commits(repo_name: str, limit: int = 20):
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        commits = []
        for commit in repo.get_commits()[:limit]:
            commits.append({
                "sha": commit.sha[:7],
                "message": commit.commit.message,
                "author": commit.commit.author.name,
                "date": str(commit.commit.author.date),
                "url": commit.html_url,
            })
        return {"commits": commits, "repo": repo_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{repo_name}/stats")
def get_repo_stats(repo_name: str):
    try:
        user = g.get_user()
        repo = user.get_repo(repo_name)
        languages = repo.get_languages()
        return {
            "name": repo.name,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "watchers": repo.watchers_count,
            "open_issues": repo.open_issues_count,
            "size": repo.size,
            "languages": languages,
            "created_at": str(repo.created_at),
            "updated_at": str(repo.updated_at),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
