"""
Issues & MR Agent
─────────────────
Searches GitLab issues and MR discussions for context related to
a file or question. Returns a summary of relevant discussions.
"""

import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import anthropic
from tools.gitlab_client import (
    search_issues,
    get_issue_notes,
)

client = anthropic.Anthropic()


def _extract_keywords(file_path: str, question: str) -> list[str]:
    """Pull search keywords from the file path and question."""
    # Use the filename without extension as a keyword
    filename = os.path.basename(file_path)
    name_without_ext = os.path.splitext(filename)[0]

    # Also extract any quoted terms or specific identifiers from question
    keywords = [name_without_ext]

    # Add directory name if it's meaningful
    parts = file_path.split("/")
    if len(parts) > 1:
        keywords.append(parts[-2])

    return list(set(keywords))


def run(file_path: str, question: str) -> dict:
    keywords = _extract_keywords(file_path, question)
    print(f"  [issues-mr] searching issues for keywords: {keywords}")

    all_issues = []
    seen_ids = set()

    for keyword in keywords:
        issues = search_issues(keyword, max_results=10)
        for issue in issues:
            if issue["id"] not in seen_ids:
                seen_ids.add(issue["id"])
                all_issues.append(issue)

    if not all_issues:
        return {
            "agent": "issues_mr",
            "summary": "No related issues or MR discussions found.",
            "issues_found": 0,
        }

    # Enrich with comments
    enriched = []
    for issue in all_issues[:8]:
        notes = get_issue_notes(issue["iid"])
        human_notes = [n for n in notes if not n.get("system", False)]
        enriched.append({
            "title": issue.get("title"),
            "url": issue.get("web_url"),
            "state": issue.get("state"),
            "created_at": issue.get("created_at", "")[:10],
            "closed_at": (issue.get("closed_at") or "")[:10],
            "description": (issue.get("description") or "")[:600],
            "labels": issue.get("labels", []),
            "comments": [n["body"][:400] for n in human_notes[:6]],
        })

    prompt = f"""You are a codebase historian analysing GitLab issues and discussions.

A developer asked: "{question}"
This relates to the file: `{file_path}`

Here are the relevant issues and discussions found:

{json.dumps(enriched, indent=2)}

Summarise what these issues reveal about the history of this code. Focus on:
- Bugs or incidents that caused changes to this file
- Design decisions discussed in issues
- Any unresolved problems or open questions
- Workarounds that were documented but never properly fixed

Be specific — mention issue titles, dates, and key quotes from discussions where relevant.
Return your summary as plain prose, 100-200 words."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "agent": "issues_mr",
        "summary": response.content[0].text,
        "issues_found": len(enriched),
        "issue_links": [{"title": i["title"], "url": i["url"], "state": i["state"]} for i in enriched],
    }


if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    question = sys.argv[2] if len(sys.argv) > 2 else "Why does this file exist?"
    result = run(file_path, question)
    print("\n── Issues & MR Agent Result ──")
    print(result["summary"])
