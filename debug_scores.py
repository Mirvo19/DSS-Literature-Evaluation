from supabase import create_client
from config import Config

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

print("=== Checking judge_scores table ===")
scores = supabase.table('judge_scores').select('*').limit(20).execute()
print(f"Total scores found: {len(scores.data)}")
for score in scores.data:
    print(f"\nScore ID: {score.get('id')}")
    print(f"  Participant ID: {score.get('participant_id')}")
    print(f"  Judge Type: {score.get('judge_type')}")
    print(f"  Score: {score.get('score')}")
    print(f"  Judge Email: {score.get('judge_email')}")

print("\n=== Checking participants for week 7e6c8e16-b7c0-44d3-83ff-62ad8b0cfdbf ===")
participants = supabase.table('participants')\
    .select('*')\
    .eq('week_id', '7e6c8e16-b7c0-44d3-83ff-62ad8b0cfdbf')\
    .execute()
print(f"Total participants: {len(participants.data)}")
for p in participants.data:
    print(f"\nParticipant ID: {p.get('id')}")
    print(f"  Student ID: {p.get('student_id')}")
    print(f"  Position: {p.get('position')}")
    print(f"  Is Winner: {p.get('is_winner')}")
