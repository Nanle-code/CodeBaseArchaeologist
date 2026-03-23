"""
CI Failure Agent
────────────────
Looks at recent failed pipelines and checks if their job logs
contain references to the file being investigated.
"""

import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import anthropic
from tools.gitlab_client import (
    get_pipelines_for_file,
    get_pipeline_jobs,
    get_job_log,
)

client = anthropic.Anthropic()


def run(file_path: str, question: str) -> dict:
    print(f"  [ci-failures] scanning recent failed pipelines...")

    filename = os.path.basename(file_path)
    pipelines = get_pipelines_for_file(file_path, max_results=20)

    if not pipelines:
        return {
            "agent": "ci_failures",
            "summary": "No failed pipelines found in recent history.",
            "pipelines_scanned": 0,
        }

    relevant_failures = []

    for pipeline in pipelines[:15]:
        jobs = get_pipeline_jobs(pipeline["id"])
        failed_jobs = [j for j in jobs if j.get("status") == "failed"]

        for job in failed_jobs[:3]:
            log = get_job_log(job["id"])
            # Only care about logs that mention our file
            if filename.lower() in log.lower() or file_path.lower() in log.lower():
                relevant_failures.append({
                    "pipeline_id": pipeline["id"],
                    "pipeline_date": pipeline.get("created_at", "")[:10],
                    "job_name": job.get("name"),
                    "job_stage": job.get("stage"),
                    "log_tail": log[-1500:],  # most relevant part
                })

    if not relevant_failures:
        return {
            "agent": "ci_failures",
            "summary": f"No CI failures found that directly reference `{file_path}`. The file may not have caused pipeline failures, or failures were in unrelated jobs.",
            "pipelines_scanned": len(pipelines),
        }

    prompt = f"""You are a CI/CD failure analyst.

A developer asked: "{question}"
This relates to the file: `{file_path}`

Here are CI pipeline failures that referenced this file:

{json.dumps(relevant_failures, indent=2)}

Summarise what these CI failures reveal. Focus on:
- What kind of failures occurred (test failures, build errors, lint issues)
- Whether there are recurring failures suggesting an ongoing problem
- Any error messages that explain WHY this code was changed
- Whether the failures appear related to the developer's question

Be specific with dates and job names. Return your summary as plain prose, 100-150 words."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "agent": "ci_failures",
        "summary": response.content[0].text,
        "failures_found": len(relevant_failures),
        "pipelines_scanned": len(pipelines),
    }


if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    question = sys.argv[2] if len(sys.argv) > 2 else "Why did this file change?"
    result = run(file_path, question)
    print("\n── CI Failure Agent Result ──")
    print(result["summary"])
