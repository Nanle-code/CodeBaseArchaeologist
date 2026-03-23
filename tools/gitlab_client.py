import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")

HEADERS = {"PRIVATE-TOKEN": GITLAB_TOKEN}


def _get(path, params=None):
    url = f"{GITLAB_URL}/api/v4{path}"
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


# ── Git history ────────────────────────────────────────────────────────────────

def get_commits_for_file(file_path, max_commits=30):
    """Return the last N commits that touched a specific file."""
    return _get(
        f"/projects/{PROJECT_ID}/repository/commits",
        params={"path": file_path, "per_page": max_commits}
    )


def get_commit_detail(commit_sha):
    """Return full diff and metadata for a single commit."""
    return _get(f"/projects/{PROJECT_ID}/repository/commits/{commit_sha}")


def get_commit_diff(commit_sha):
    """Return the file diffs introduced by a commit."""
    return _get(f"/projects/{PROJECT_ID}/repository/commits/{commit_sha}/diff")


def get_file_blame(file_path, ref="main"):
    """Return blame data — who wrote each line and in which commit."""
    return _get(
        f"/projects/{PROJECT_ID}/repository/files/{requests.utils.quote(file_path, safe='')}/blame",
        params={"ref": ref}
    )


# ── Issues & Merge Requests ────────────────────────────────────────────────────

def search_issues(keyword, max_results=20):
    """Search issues by keyword."""
    return _get(
        f"/projects/{PROJECT_ID}/issues",
        params={"search": keyword, "per_page": max_results, "state": "all"}
    )


def get_issue_notes(issue_iid):
    """Return all comments on an issue."""
    return _get(
        f"/projects/{PROJECT_ID}/issues/{issue_iid}/notes",
        params={"per_page": 100}
    )


def get_merge_requests_for_commit(commit_sha):
    """Return MRs associated with a commit."""
    return _get(
        f"/projects/{PROJECT_ID}/repository/commits/{commit_sha}/merge_requests"
    )


def get_mr_notes(mr_iid):
    """Return all comments on a merge request."""
    return _get(
        f"/projects/{PROJECT_ID}/merge_requests/{mr_iid}/notes",
        params={"per_page": 100}
    )


# ── CI Pipelines ───────────────────────────────────────────────────────────────

def get_pipelines_for_file(file_path, max_results=20):
    """Return recent pipelines. We'll filter by file path in the agent."""
    return _get(
        f"/projects/{PROJECT_ID}/pipelines",
        params={"per_page": max_results, "status": "failed"}
    )


def get_pipeline_jobs(pipeline_id):
    """Return all jobs in a pipeline."""
    return _get(f"/projects/{PROJECT_ID}/pipelines/{pipeline_id}/jobs")


def get_job_log(job_id, max_chars=3000):
    """Return the raw log for a CI job (truncated)."""
    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/jobs/{job_id}/trace"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text[-max_chars:]  # tail of log is most useful
    return ""
