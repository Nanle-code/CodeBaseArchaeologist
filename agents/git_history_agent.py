"""
Git History Agent
─────────────────
Takes a file path + optional line range, retrieves commit history,
diffs, and associated MRs, then asks Claude to summarise the story.
"""

import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import anthropic
from tools.gitlab_client import (
    get_commits_for_file,
    get_commit_detail,
    get_commit_diff,
    get_merge_requests_for_commit,
    get_mr_notes,
)

client = anthropic.Anthropic()


def run(file_path: str, question: str, max_commits: int = 15) -> dict:
    print(f"  [git-history] fetching commits for {file_path}...")
    commits = get_commits_for_file(file_path, max_commits)

    if not commits:
        return {"agent": "git_history", "summary": "No commit history found for this file.", "raw": []}

    # Collect rich data for the most relevant commits
    enriched = []
    for commit in commits[:10]:
        sha = commit["id"]
        detail = get_commit_detail(sha)
        diff = get_commit_diff(sha)

        # Only keep diff hunks that touch our file
        relevant_diffs = [d for d in diff if file_path in d.get("new_path", "")]

        mrs = get_merge_requests_for_commit(sha)
        mr_discussions = []
        for mr in mrs[:2]:
            notes = get_mr_notes(mr["iid"])
            # Filter out system notes, keep human comments
            human_notes = [n for n in notes if not n.get("system", False)]
            mr_discussions.append({
                "title": mr.get("title"),
                "url": mr.get("web_url"),
                "description": mr.get("description", "")[:500],
                "comments": [n["body"][:300] for n in human_notes[:5]],
            })

        enriched.append({
            "sha": sha[:8],
            "author": commit.get("author_name"),
            "date": commit.get("created_at", "")[:10],
            "message": commit.get("message", "").strip(),
            "diffs": [{"path": d["new_path"], "diff": d.get("diff", "")[:800]} for d in relevant_diffs],
            "merge_requests": mr_discussions,
        })

    # Ask Claude to make sense of it
    prompt = f"""You are a git history analyst. A developer asked: "{question}"

Here is the commit history for the file `{file_path}`:

{json.dumps(enriched, indent=2)}

Summarise the history of this file in plain English. Focus on:
- The most significant changes and why they happened
- Any interesting decisions visible in commit messages or MR discussions
- How the file evolved over time
- Specific answers to the developer's question if the evidence supports it

Be concise but include specific details (dates, authors, commit messages) that help tell the story.
Return your summary as plain prose, 150-250 words."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "agent": "git_history",
        "summary": response.content[0].text,
        "commits_analysed": len(enriched),
        "raw_commits": [{"sha": c["sha"], "date": c["date"], "message": c["message"]} for c in enriched],
    }


if __name__ == "__main__":
    # Quick test
    file_path = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    question = sys.argv[2] if len(sys.argv) > 2 else "Why does this file look the way it does?"
    result = run(file_path, question)
    print("\n── Git History Agent Result ──")
    print(result["summary"])
