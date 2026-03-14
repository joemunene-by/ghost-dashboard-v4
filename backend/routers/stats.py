from fastapi import APIRouter, HTTPException
from github import Github
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

router = APIRouter()
g = Github(os.getenv("GITHUB_TOKEN"))

@router.get("/overview")
def get_overview():
    try:
        user = g.get_user()
        repos = list(user.get_repos())
        total_stars = sum(r.stargazers_count for r in repos)
        total_forks = sum(r.forks_count for r in repos)
        languages = {}
        for repo in repos:
            if repo.language:
                languages[repo.language] = languages.get(repo.language, 0) + 1
        return {
            "username": user.login,
            "name": user.name,
            "total_repos": len(repos),
            "public_repos": user.public_repos,
            "total_stars": total_stars,
            "total_forks": total_forks,
            "followers": user.followers,
            "following": user.following,
            "top_languages": dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/heatmap")
def get_heatmap():
    try:
        user = g.get_user()
        since = datetime.now() - timedelta(days=365)
        contributions = {}
        for repo in user.get_repos():
            try:
                for commit in repo.get_commits(since=since, author=user.login):
                    date = str(commit.commit.author.date.date())
                    contributions[date] = contributions.get(date, 0) + 1
            except:
                continue
        return {"heatmap": contributions, "total_commits": sum(contributions.values())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
