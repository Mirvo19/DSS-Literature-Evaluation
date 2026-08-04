"""remove qa seed data from dss talk. this script deletes only rows that were created by seer.py."""

from __future__ import annotations

import sys
from typing import Any, Dict, List
from pathlib import Path

from supabase import create_client

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config


SEED_MARKER = "QA Seed"
SEED_ADMIN_EMAIL = "qa.seed.admin@dss-talk.test"
SEED_EMAIL_PREFIX = "qa.seed."


def client():
    if not Config.SUPABASE_URL or not Config.SUPABASE_SERVICE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
    return create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)


SUPABASE = client()


def fetch_all(table_name: str, select: str = "*") -> List[Dict[str, Any]]:
    response = SUPABASE.table(table_name).select(select).execute()
    return response.data or []


def delete_ids(table_name: str, ids: List[str]) -> None:
    for row_id in ids:
        SUPABASE.table(table_name).delete().eq("id", row_id).execute()


def seeded_auth_users() -> List[Dict[str, Any]]:
    users: List[Dict[str, Any]] = []
    page = 1
    while True:
        page_users = SUPABASE.auth.admin.list_users(page=page, per_page=200)
        if not page_users:
            break
        users.extend(
            {"id": user.id, "email": user.email}
            for user in page_users
            if user.email and (user.email == SEED_ADMIN_EMAIL or user.email.startswith(SEED_EMAIL_PREFIX))
        )
        if len(page_users) < 200:
            break
        page += 1
    return users


def main() -> None:
    # remove leaf data first.
    judge_score_ids = [row["id"] for row in fetch_all("judge_scores") if SEED_MARKER in (row.get("comments") or "")]
    delete_ids("judge_scores", judge_score_ids)

    audit_log_ids = [
        row["id"]
        for row in fetch_all("audit_logs")
        if SEED_MARKER in (row.get("entity_name") or "") or SEED_MARKER in (row.get("description") or "")
    ]
    delete_ids("audit_logs", audit_log_ids)

    for table, field in (
        ("participants", "notes"),
        ("week_judges", None),
        ("week_criteria", None),
        ("judge_permissions", "user_email"),
        ("session_speaker_status", None),
        ("weeks", "notes"),
        ("sessions", "name"),
        ("judges", "full_name"),
        ("students", "full_name"),
        ("judging_criteria", "description"),
    ):
        rows = fetch_all(table)
        if field is None:
            ids = [row["id"] for row in rows if SEED_MARKER in str(row)]
        else:
            ids = [row["id"] for row in rows if SEED_MARKER in (row.get(field) or "") or (field == "user_email" and (row.get(field) or "").startswith(SEED_EMAIL_PREFIX))]
        delete_ids(table, ids)

    # remove seed-created events only if they were created by the seeder.
    event_rows = fetch_all("events")
    event_ids = [row["id"] for row in event_rows if (row.get("description") or "") == f"{SEED_MARKER} event for QA coverage"]
    delete_ids("events", event_ids)

    removed_users = seeded_auth_users()
    admin_rows = fetch_all("admins")
    admin_ids = [row["id"] for row in admin_rows if row.get("user_id") in {user["id"] for user in removed_users}]
    delete_ids("admins", admin_ids)

    for user in removed_users:
        SUPABASE.auth.admin.delete_user(user["id"])

    print("Unseed complete")
    print(f"Removed auth users: {len(removed_users)}")


if __name__ == "__main__":
    main()
