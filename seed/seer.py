"""Seed DSS Talk with QA data.

This script creates a deterministic, tagged dataset that exercises the main
admin, dashboard, judging, and results flows.
"""

from __future__ import annotations

import os
import sys
from datetime import date, timedelta
from typing import Any, Dict, List, Optional
from pathlib import Path

from supabase import create_client

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config


SEED_MARKER = "QA Seed"
SEED_ADMIN_EMAIL = "qa.seed.admin@dss-talk.test"
SEED_ADMIN_PASSWORD = os.getenv("QA_SEED_ADMIN_PASSWORD", "QA-Seed-Admin-123!")
SEED_JUDGES = [
    {
        "role": "overall",
        "email": "qa.seed.overall@dss-talk.test",
        "password": os.getenv("QA_SEED_OVERALL_PASSWORD", "QA-Seed-Overall-123!"),
        "full_name": "QA Seed Overall Judge",
        "title": "Overall Judge",
    },
    {
        "role": "content",
        "email": "qa.seed.content@dss-talk.test",
        "password": os.getenv("QA_SEED_CONTENT_PASSWORD", "QA-Seed-Content-123!"),
        "full_name": "QA Seed Content Judge",
        "title": "Content Judge",
    },
    {
        "role": "style_delivery",
        "email": "qa.seed.style@dss-talk.test",
        "password": os.getenv("QA_SEED_STYLE_PASSWORD", "QA-Seed-Style-123!"),
        "full_name": "QA Seed Style Judge",
        "title": "Style & Delivery Judge",
    },
    {
        "role": "language",
        "email": "qa.seed.language@dss-talk.test",
        "password": os.getenv("QA_SEED_LANGUAGE_PASSWORD", "QA-Seed-Language-123!"),
        "full_name": "QA Seed Language Judge",
        "title": "Language Judge",
    },
]

EVENTS = [
    {
        "name": "Debate",
        "name_nepali": "बहस",
        "description": f"{SEED_MARKER} event for QA coverage",
    },
    {
        "name": "Presentation",
        "name_nepali": "प्रस्तुतीकरण",
        "description": f"{SEED_MARKER} event for QA coverage",
    },
    {
        "name": "Extempore",
        "name_nepali": "तत्काल भाषण",
        "description": f"{SEED_MARKER} event for QA coverage",
    },
]

CRITERIA = [
    {
        "name": "Overall Impact",
        "name_nepali": "समग्र प्रभाव",
        "description": "QA seed overall assessment",
        "category": "overall",
        "max_points": 25,
    },
    {
        "name": "Content Quality",
        "name_nepali": "विषयवस्तु गुणस्तर",
        "description": "QA seed content assessment",
        "category": "content",
        "max_points": 25,
    },
    {
        "name": "Style and Delivery",
        "name_nepali": "शैली र प्रस्तुति",
        "description": "QA seed style assessment",
        "category": "style_delivery",
        "max_points": 25,
    },
    {
        "name": "Language Use",
        "name_nepali": "भाषा प्रयोग",
        "description": "QA seed language assessment",
        "category": "language",
        "max_points": 25,
    },
]

STUDENTS = [
    {"full_name": f"QA Seed Student {index:02d}", "grade": 11 if index % 2 else 12, "email": f"qa.seed.student{index:02d}@dss-talk.test"}
    for index in range(1, 13)
]

JUDGE_TYPE_TO_SCORE = {
    "overall": 22.5,
    "content": 23.75,
    "style_delivery": 21.25,
    "language": 22.0,
}


SUPABASE = None
SEED_ADMIN = None


def client():
    if not Config.SUPABASE_URL or not Config.SUPABASE_SERVICE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
    return create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)


def first(table_name: str, **filters: Any) -> Optional[Dict[str, Any]]:
    query = SUPABASE.table(table_name).select("*")
    for field, value in filters.items():
        query = query.eq(field, value)
    response = query.limit(1).execute()
    return response.data[0] if response.data else None


def find_by_email(email: str) -> Optional[Dict[str, Any]]:
    page = 1
    while True:
        users = SUPABASE.auth.admin.list_users(page=page, per_page=200)
        if not users:
            return None
        for user in users:
            if user.email == email:
                return {"id": user.id, "email": user.email}
        if len(users) < 200:
            return None
        page += 1


def ensure_auth_user(email: str, password: str, full_name: str, role: str) -> Dict[str, Any]:
    existing = find_by_email(email)
    if existing:
        return existing

    response = SUPABASE.auth.admin.create_user(
        {
            "email": email,
            "password": password,
            "email_confirm": True,
            "user_metadata": {"full_name": full_name, "seed_role": role, "seed_marker": SEED_MARKER},
        }
    )
    return {"id": response.user.id, "email": response.user.email}


def ensure_row(table_name: str, lookup: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    existing = first(table_name, **lookup)
    if existing:
        return existing

    response = SUPABASE.table(table_name).insert(payload).execute()
    return response.data[0]


def get_event(name: str) -> Dict[str, Any]:
    existing = first("events", name=name)
    if existing:
        return existing
    event_data = next(event for event in EVENTS if event["name"] == name)
    return ensure_row("events", {"name": name}, event_data)


def seed_students() -> List[Dict[str, Any]]:
    students = []
    for student in STUDENTS:
        students.append(
            ensure_row(
                "students",
                {"full_name": student["full_name"]},
                {
                    "full_name": student["full_name"],
                    "grade": student["grade"],
                    "email": student["email"],
                    "is_active": True,
                },
            )
        )
    return students


def seed_judges() -> List[Dict[str, Any]]:
    judges = []
    for judge in SEED_JUDGES:
        judges.append(
            ensure_row(
                "judges",
                {"email": judge["email"]},
                {
                    "full_name": judge["full_name"],
                    "title": judge["title"],
                    "email": judge["email"],
                    "is_active": True,
                },
            )
        )
    return judges


def seed_criteria() -> List[Dict[str, Any]]:
    criteria = []
    for criterion in CRITERIA:
        criteria.append(
            ensure_row(
                "judging_criteria",
                {"name": criterion["name"], "category": criterion["category"]},
                criterion,
            )
        )
    return criteria


def seed_sessions_and_weeks(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seeded_weeks: List[Dict[str, Any]] = []
    base_day = date(2026, 7, 1)

    for event_index, event in enumerate(events):
        event_name = event["name"]
        for language_index, language in enumerate(("en", "ne")):
            session = ensure_row(
                "sessions",
                {"event_id": event["id"], "session_number": 1, "language": language},
                {
                    "event_id": event["id"],
                    "name": f"{SEED_MARKER} {event_name} Session {language.upper()}",
                    "session_number": 1,
                    "language": language,
                    "start_date": str(base_day + timedelta(days=event_index * 14 + language_index * 7)),
                    "end_date": str(base_day + timedelta(days=event_index * 14 + language_index * 7 + 1)),
                    "is_active": True,
                },
            )

            week = ensure_row(
                "weeks",
                {"session_id": session["id"], "week_number": 1},
                {
                    "session_id": session["id"],
                    "week_number": 1,
                    "topic": f"{SEED_MARKER} {event_name} topic ({language.upper()})",
                    "topic_nepali": f"{SEED_MARKER} {event_name} विषय ({language.upper()})",
                    "date": str(base_day + timedelta(days=event_index * 14 + language_index * 7)),
                    "is_partial": False,
                    "notes": f"{SEED_MARKER} week for QA",
                },
            )

            seeded_weeks.append({"event": event, "session": session, "week": week, "language": language})

    return seeded_weeks


def seed_week_judges(week_id: str, judges: List[Dict[str, Any]]) -> None:
    for judge in judges:
        ensure_row(
            "week_judges",
            {"week_id": week_id, "judge_id": judge["id"]},
            {"week_id": week_id, "judge_id": judge["id"]},
        )


def seed_week_criteria(week_id: str, criteria: List[Dict[str, Any]]) -> None:
    for criterion in criteria:
        ensure_row(
            "week_criteria",
            {"week_id": week_id, "criteria_id": criterion["id"]},
            {"week_id": week_id, "criteria_id": criterion["id"]},
        )


def seed_participants(week_id: str, students: List[Dict[str, Any]], offset: int) -> List[Dict[str, Any]]:
    participants = []
    for index in range(4):
        student = students[(offset + index) % len(students)]
        participants.append(
            ensure_row(
                "participants",
                {"week_id": week_id, "student_id": student["id"]},
                {
                    "week_id": week_id,
                    "student_id": student["id"],
                    "score": 0,
                    "is_winner": False,
                    "position": None,
                    "notes": f"{SEED_MARKER} participant",
                },
            )
        )
    return participants


def seed_speaker_status(session_id: str, week_id: str, students: List[Dict[str, Any]], offset: int) -> None:
    for index in range(4):
        student = students[(offset + index) % len(students)]
        ensure_row(
            "session_speaker_status",
            {"session_id": session_id, "student_id": student["id"]},
            {
                "session_id": session_id,
                "student_id": student["id"],
                "has_spoken": index < 2,
                "spoken_in_week_id": week_id if index < 2 else None,
            },
        )


def seed_permissions(week_id: str, judges: List[Dict[str, Any]]) -> None:
    for judge in judges:
        ensure_row(
            "judge_permissions",
            {"user_email": judge["email"], "week_id": week_id, "judge_type": judge["role"]},
            {
                "user_email": judge["email"],
                "week_id": week_id,
                "judge_type": judge["role"],
                "is_active": True,
                "granted_by_admin_email": SEED_ADMIN_EMAIL,
            },
        )


def score_value(event_index: int, week_index: int, participant_index: int, role: str) -> float:
    base = 68 + event_index * 2 + week_index * 1.5 + participant_index * 1.25
    return round(base + JUDGE_TYPE_TO_SCORE[role], 2)


def seed_scores_and_rankings(week: Dict[str, Any], event_index: int, week_index: int, participants: List[Dict[str, Any]], judges: List[Dict[str, Any]]) -> None:
    totals: Dict[str, float] = {}

    for participant_index, participant in enumerate(participants):
        total = 0.0
        for judge in judges:
            score = score_value(event_index, week_index, participant_index, judge["role"])
            total += score
            ensure_row(
                "judge_scores",
                {
                    "participant_id": participant["id"],
                    "judge_email": judge["email"],
                    "judge_type": judge["role"],
                },
                {
                    "participant_id": participant["id"],
                    "judge_email": judge["email"],
                    "judge_type": judge["role"],
                    "score": score,
                    "max_score": 100,
                    "comments": f"{SEED_MARKER} {judge['role']} score",
                    "criteria_breakdown": {"seed": True, "role": judge["role"]},
                },
            )
        totals[participant["id"]] = round(total, 2)

    ordered = sorted(participants, key=lambda participant: totals[participant["id"]], reverse=True)
    for position, participant in enumerate(ordered, start=1):
        SUPABASE.table("participants").update(
            {
                "score": totals[participant["id"]],
                "position": position,
                "is_winner": position <= 3,
            }
        ).eq("id", participant["id"]).execute()

    SUPABASE.table("audit_logs").insert(
        {
            "admin_email": SEED_ADMIN_EMAIL,
            "admin_id": SEED_ADMIN.get("id"),
            "action_type": "UPDATE",
            "entity_type": "week",
            "entity_id": week["id"],
            "entity_name": f"{SEED_MARKER} Week {week['week_number']}",
            "description": f"{SEED_MARKER} published results for week {week['week_number']}",
            "new_value": {"published": True, "participant_count": len(participants)},
        }
    ).execute()


def main() -> None:
    global SUPABASE, SEED_ADMIN

    SUPABASE = client()

    SEED_ADMIN = ensure_auth_user(SEED_ADMIN_EMAIL, SEED_ADMIN_PASSWORD, "QA Seed Admin", "admin")
    admin_row = ensure_row(
        "admins",
        {"user_id": SEED_ADMIN["id"]},
        {"user_id": SEED_ADMIN["id"]},
    )

    seed_events = [get_event(event["name"]) for event in EVENTS]
    students = seed_students()
    judges = seed_judges()
    criteria = seed_criteria()
    weeks = seed_sessions_and_weeks(seed_events)

    for week_index, week_bundle in enumerate(weeks):
        week = week_bundle["week"]
        session = week_bundle["session"]
        event = week_bundle["event"]
        event_index = next(index for index, candidate in enumerate(seed_events) if candidate["id"] == event["id"])

        seed_week_judges(week["id"], judges)
        seed_week_criteria(week["id"], criteria)
        seed_permissions(week["id"], judges)

        participants = seed_participants(week["id"], students, week_index * 2)
        seed_speaker_status(session["id"], week["id"], students, week_index * 2)
        seed_scores_and_rankings(week, event_index, week_index, participants, judges)

    print("Seed complete")
    print(f"Admin: {SEED_ADMIN_EMAIL}")
    for judge in SEED_JUDGES:
        print(f"Judge: {judge['email']} ({judge['role']})")
    print("Students:", ", ".join(student["email"] for student in STUDENTS))
    print(f"Admin row id: {admin_row['id']}")


if __name__ == "__main__":
    main()