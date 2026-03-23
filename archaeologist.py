"""
Codebase Archaeologist — Orchestrator
──────────────────────────────────────
Main entry point. Takes a file path and a question, fans out to
all three specialist agents concurrently, then synthesises the
results into a single narrative answer.

Usage:
    python archaeologist.py <file_path> "<question>"

Example:
    python archaeologist.py src/payments/processor.py "Why is the timeout set to 47000?"
"""

import sys
import os
import json
import concurrent.futures
import anthropic

sys.path.insert(0, os.path.dirname(__file__))

from agents.git_history_agent import run as run_git_history
from agents.issues_mr_agent import run as run_issues_mr
from agents.ci_failure_agent import run as run_ci_failures

client = anthropic.Anthropic()


def synthesise(file_path: str, question: str, results: list[dict]) -> str:
    """Take the three agent summaries and produce a single narrative."""

    git_result   = next((r for r in results if r["agent"] == "git_history"),  {})
    issues_result = next((r for r in results if r["agent"] == "issues_mr"),   {})
    ci_result    = next((r for r in results if r["agent"] == "ci_failures"),  {})

    prompt = f"""You are the Codebase Archaeologist. A developer asked:

"{question}"

About this file: `{file_path}`

Three specialist agents have gathered evidence from the repository. Your job is to
synthesise their findings into a single, clear narrative that directly answers
the developer's question.

═══ Git History Agent ═══
{git_result.get("summary", "No data.")}

═══ Issues & MR Agent ═══
{issues_result.get("summary", "No data.")}

═══ CI Failures Agent ═══
{ci_result.get("summary", "No data.")}

Write a concise, narrative answer (200-350 words) that:
1. Directly addresses the developer's question in the first sentence
2. Tells the story chronologically where relevant
3. Cites specific evidence (dates, commit messages, issue titles, author names)
4. Flags any unresolved questions or things that couldn't be determined
5. Ends with a one-sentence "bottom line"

Write in a clear, helpful tone — like a senior engineer who's read the whole history."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def dig(file_path: str, question: str) -> dict:
    print(f"\nCodebase Archaeologist")
    print(f"File   : {file_path}")
    print(f"Question: {question}")
    print(f"\nDispatching agents...\n")

    # Run all three agents concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_git    = executor.submit(run_git_history, file_path, question)
        future_issues = executor.submit(run_issues_mr,   file_path, question)
        future_ci     = executor.submit(run_ci_failures, file_path, question)

        results = []
        for future in concurrent.futures.as_completed([future_git, future_issues, future_ci]):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"  [warning] agent failed: {e}")

    print(f"\nSynthesising findings...\n")
    narrative = synthesise(file_path, question, results)

    return {
        "question": question,
        "file": file_path,
        "answer": narrative,
        "sources": {
            "commits_analysed": next((r.get("commits_analysed", 0) for r in results if r["agent"] == "git_history"), 0),
            "issues_found":     next((r.get("issues_found", 0)     for r in results if r["agent"] == "issues_mr"),   0),
            "ci_failures_found": next((r.get("failures_found", 0)  for r in results if r["agent"] == "ci_failures"), 0),
        },
        "raw_agent_summaries": {r["agent"]: r["summary"] for r in results},
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python archaeologist.py <file_path> \"<question>\"")
        print("Example: python archaeologist.py src/auth.py \"Why is the session timeout 47 seconds?\"")
        sys.exit(1)

    file_path = sys.argv[1]
    question  = " ".join(sys.argv[2:])

    result = dig(file_path, question)

    print("═" * 60)
    print("ANSWER")
    print("═" * 60)
    print(result["answer"])
    print()
    print(f"Sources: {result['sources']['commits_analysed']} commits · "
          f"{result['sources']['issues_found']} issues · "
          f"{result['sources']['ci_failures_found']} CI failures")
    print("═" * 60)


if __name__ == "__main__":
    main()
