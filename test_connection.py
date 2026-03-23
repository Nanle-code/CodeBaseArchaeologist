"""
Day 1 sanity check — run this first to verify your GitLab
credentials and project ID are working before touching the agents.

Usage:
    python test_connection.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from tools.gitlab_client import _get, PROJECT_ID, GITLAB_TOKEN, GITLAB_URL


def check(label, fn):
    try:
        result = fn()
        print(f"  ✓ {label}")
        return result
    except Exception as e:
        print(f"  ✗ {label} — {e}")
        return None


print("\nCodebase Archaeologist — Connection Test")
print("=" * 42)

# 1. Token present
if not GITLAB_TOKEN or GITLAB_TOKEN == "your_personal_access_token_here":
    print("  ✗ GITLAB_TOKEN not set in .env")
    sys.exit(1)
print(f"  ✓ Token loaded (ends in ...{GITLAB_TOKEN[-4:]})")
print(f"  ✓ GitLab URL: {GITLAB_URL}")
print(f"  ✓ Project ID: {PROJECT_ID}")

# 2. Can reach GitLab
project = check(
    "GitLab API reachable",
    lambda: _get(f"/projects/{PROJECT_ID}")
)

if project:
    print(f"\n  Project name : {project.get('name')}")
    print(f"  Default branch: {project.get('default_branch')}")
    print(f"  Visibility   : {project.get('visibility')}")

# 3. Can read commits
commits = check(
    "Can read commit history",
    lambda: _get(f"/projects/{PROJECT_ID}/repository/commits", {"per_page": 3})
)
if commits:
    print(f"\n  Last 3 commits:")
    for c in commits:
        print(f"    {c['short_id']} ({c['created_at'][:10]}) — {c['title'][:60]}")

# 4. Can read issues
issues = check(
    "Can read issues",
    lambda: _get(f"/projects/{PROJECT_ID}/issues", {"per_page": 3, "state": "all"})
)
if issues:
    print(f"\n  Found {len(issues)} issues (showing up to 3)")

print("\n" + "=" * 42)
if project and commits:
    print("All good! You're ready to run the archaeologist.")
    print("\nNext step:")
    print(f"  python archaeologist.py <any_file_in_your_repo> \"your question\"")
else:
    print("Fix the errors above before proceeding.")
