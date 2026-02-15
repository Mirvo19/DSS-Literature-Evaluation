# DSS Talk Event Management System - Complete Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [Getting Started](#getting-started)
3. [Architecture](#architecture)
4. [Features](#features)
5. [Database Schema](#database-schema)
6. [API Reference](#api-reference)
7. [Judging System](#judging-system)
8. [Deployment Guide](#deployment-guide)
9. [User Guide](#user-guide)
10. [Admin Guide](#admin-guide)
11. [Troubleshooting](#troubleshooting)

---

## System Overview

DSS Talk is a full-stack web application designed for managing school speaking events including Debate, Presentation, and Extempore competitions. The system provides bilingual support (English/Nepali) and includes comprehensive administrative tools for managing students, sessions, scoring, and publishing results.

### Technology Stack

**Backend:**
- Python 3.8+ with Flask 3.0
- Supabase Python Client for database operations
- JWT-based authentication via Supabase Auth

**Frontend:**
- Vanilla JavaScript (no build process required)
- Modern CSS with Grid and Flexbox
- Responsive design for mobile and desktop

**Database:**
- PostgreSQL via Supabase
- Row Level Security for access control
- Automated triggers and views

### Key Capabilities

- Multi-event management (Debate, Presentation, Extempore)
- Temporary judge permissions with role-based scoring
- Intelligent random participant selection for Extempore
- CSV bulk import for student data
- Complete audit logging of admin actions
- Published results with position rankings
- Bilingual interface with persistent language preferences

---

## Getting Started

### Prerequisites

Before setting up the application, ensure you have:

- Python 3.8 or higher installed
- A Supabase account (free tier is sufficient)
- Basic understanding of command line operations
- A text editor or IDE

### Initial Setup Steps

**1. Create Supabase Project**

Visit [supabase.com](https://supabase.com) and create a new project. Save the following credentials:
- Project URL
- Anon/Public API Key
- Service Role Key (keep this secret)

**2. Setup Database**

Navigate to the SQL Editor in your Supabase dashboard and run the complete schema:
- Open `database/MASTER_SCHEMA.sql`
- Copy all contents
- Paste into SQL Editor
- Execute the query

This will create all tables, indexes, policies, triggers, and default data.

**3. Clone and Configure**

```bash
# Clone or download the repository
cd Ver1

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

**4. Configure Environment Variables**

Edit the `.env` file with your Supabase credentials:

```
FLASK_SECRET_KEY=your-random-secret-key-here
FLASK_ENV=development

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
```

**5. Run the Application**

```bash
python app.py
```

Open your browser to `http://localhost:5000`

**6. Create Admin User**

First, sign up for an account through the application. Then:

1. Go to Supabase Dashboard → Authentication → Users
2. Copy the user's UUID
3. In SQL Editor, run:
   ```sql
   INSERT INTO admins (user_id) VALUES ('paste-uuid-here');
   ```

You now have full admin access.

---

## Architecture

### Project Structure

```
Ver1/
├── app.py                      # Application entry point
├── config.py                   # Environment configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .gitignore                  # Git ignore patterns
│
├── database/
│   └── MASTER_SCHEMA.sql       # Complete database schema
│
├── routes/
│   ├── auth.py                 # Authentication endpoints
│   ├── events.py               # Public event endpoints
│   ├── admin.py                # Admin management endpoints
│   └── judge.py                # Judge scoring endpoints
│
├── utils/
│   ├── auth.py                 # Authentication decorators
│   ├── csv_handler.py          # CSV import logic
│   ├── random_selector.py      # Extempore selection algorithm
│   └── audit_logger.py         # Action logging utility
│
├── static/
│   ├── css/
│   │   └── styles.css          # Application styles
│   └── js/
│       ├── i18n.js             # Internationalization
│       ├── auth.js             # Client auth logic
│       ├── main.js             # Main application
│       └── admin.js            # Admin panel logic
│
└── templates/
    ├── login.html              # Login page
    ├── signup.html             # Registration page
    ├── dashboard.html          # User dashboard
    ├── winners.html            # Published results
    ├── week-rankings.html      # Detailed rankings
    ├── admin/
    │   ├── dashboard.html      # Admin home
    │   ├── students.html       # Student management
    │   ├── sessions.html       # Session management
    │   ├── weeks.html          # Week management
    │   ├── results.html        # Results and publishing
    │   └── judge_permissions.html
    └── judge/
        └── scoring.html        # Judge scoring interface
```

### Data Flow

**Authentication Flow:**
1. User submits credentials via login form
2. Supabase Auth validates and returns JWT token
3. Token stored in localStorage
4. All API requests include token in Authorization header
5. Server validates token on protected routes
6. Admin routes check user_id in admins table

**Scoring Flow:**
1. Admin grants judge permissions for specific week/type
2. Judge logs in and sees assigned participants
3. Judge submits scores with criteria breakdown
4. Scores stored in judge_scores table
5. Admin views aggregated results
6. Admin publishes results (calculates positions)
7. Published results appear on winners page

**Extempore Selection Flow:**
1. Admin creates new week with participant_mode='random'
2. System queries active students in specified grade
3. Excludes students who have spoken in current session
4. Randomly selects required number
5. Marks selected students in session_speaker_status
6. Creates participant records
7. If insufficient students, offers partial week or reset

---

## Features

### Authentication System

**User Registration**
- Email and password based
- Email validation
- Password strength requirements
- Automatic account creation in Supabase Auth

**Login**
- Session token stored locally
- Persistent login (until logout)
- Automatic redirection based on role
- Session expiration handling

**Admin Access**
- Separate admin table for authorization
- Cannot be created via signup
- Requires manual database insertion
- Server-side verification on all admin routes

### Bilingual Support

**Language Switching**
- Toggle between English and Nepali
- Instant UI update without reload
- Preference stored in localStorage
- Database content includes both languages where applicable

**Translation Coverage**
- All UI labels and messages
- Event names
- Judging criteria
- Week topics
- Form labels and buttons

### Event Management

**Event Types**
1. **Debate**: Formal debate competitions
2. **Presentation**: Presentation competitions
3. **Extempore**: Impromptu speaking with intelligent selection

**Session Management**
- Sessions group weeks within an event
- Track start and end dates
- Active/inactive status
- Unique session numbers per event

**Week Management**
- Individual competition weeks within sessions
- Topic assignment (English and Nepali)
- Date tracking
- Participant management
- Judge assignments
- Custom criteria selection

### Judging System

**Judge Types**
- Overall Judge: 10 points total
- Content Judge: 10 points total
- Style & Delivery Judge: 10 points total
- Language Judge: 10 points total

**Permissions**
- Temporary access granted per week
- Role-specific (judge type)
- Can be revoked by admin
- Reactivatable for subsequent weeks

**Scoring**
- Criteria-based breakdown
- Comments per participant
- Real-time validation
- Edit capability
- Automatic total calculation

**Results Publishing**
- Aggregates all judge scores
- Calculates total for each participant
- Assigns positions (1st, 2nd, 3rd, etc.)
- Marks top 3 as winners
- Publish/unpublish toggle

### Student Management

**Manual Entry**
- Add individual students
- Edit student details
- Activate/deactivate students
- Grade assignment

**CSV Import**
- Bulk upload capability
- Format: `full_name,grade`
- Duplicate detection
- Validation and error reporting
- Preview before import

**Grade Filtering**
- Filter by grade 11 or 12
- Used in Extempore selection
- Optional filtering in admin views

### Random Selection (Extempore)

**Selection Algorithm**
1. Get all active students in specified grade (if filtered)
2. Query session_speaker_status for current session
3. Exclude students where has_spoken=true
4. Randomly sample required number
5. Create participant records
6. Update speaker_status table

**Edge Cases**
- Insufficient students: Offer partial week or reset
- No available students: Require session reset
- Manual override: Admin can select manually
- Reset session: Clears has_spoken flags

**Settings**
- Participant count (default: 5)
- Grade filter (optional)
- Reset if insufficient (checkbox)

### Winners and Rankings

**Winners Page**
- Lists weeks with published results
- Filter by event
- Shows week topic and date
- "View Rankings" button per week

**Rankings Page**
- Full ranking table for specific week
- Shows top 3 with position medals
- Individual judge scores displayed
- Total score calculation
- Student details (name, grade)

---

## Database Schema

### Core Tables

**admins**
- Stores user IDs of administrators
- References auth.users table
- Required for admin panel access

**events**
- Main event types (Debate, Presentation, Extempore)
- Bilingual names
- Seeded with default events

**sessions**
- Competition sessions within events
- Track active status
- Unique session numbers

**students**
- Student roster
- Grade tracking
- Active/inactive status

**weeks**
- Individual weeks within sessions
- Topic in English and Nepali
- Date and notes fields
- Partial week flag

**participants**
- Links students to weeks
- Stores position and winner status
- Initially used for score tracking (now uses judge_scores)

### Judging Tables

**judge_permissions**
- Temporary judge access
- Week and judge type specific
- Grant and revoke tracking
- Admin email audit trail

**judge_scores**
- Detailed scores by judge type
- Criteria breakdown in JSON
- Comments field
- Unique constraint per participant/judge/type

**judging_criteria**
- Evaluation criteria definitions
- Category-based (overall, content, style_delivery, language)
- Max points per criterion
- Bilingual names

### Tracking Tables

**session_speaker_status**
- Tracks Extempore participation
- Session-specific
- Links to week where student spoke
- Used for intelligent selection

**audit_logs**
- Complete action history
- Admin email and timestamp
- Entity type and ID
- Old and new values in JSON
- Description field

### Relationships

```
events (1) ──< (many) sessions
sessions (1) ──< (many) weeks
weeks (1) ──< (many) participants
students (1) ──< (many) participants
weeks (1) ──< (many) judge_permissions
participants (1) ──< (many) judge_scores
judging_criteria (1) ──< (many) [used in scoring]
```

### Views

**recent_winners**
- Pre-joined winner data
- Sorted by date descending
- Includes student, week, session, event info

**week_details**
- Aggregated week information
- Participant, judge, criteria counts
- Simplified queries

---

## API Reference

### Public Endpoints

**GET /** - Login page

**GET /signup** - Registration page

**POST /auth/signup**
- Body: `{email, password}`
- Returns: Success message or error

**POST /auth/login**
- Body: `{email, password}`
- Returns: `{user, session, is_admin}`

**POST /auth/logout**
- Headers: Authorization token
- Returns: Success message

### Authenticated Endpoints

**GET /dashboard**
- Returns: Dashboard HTML
- Requires: Valid auth token

**GET /api/events**
- Returns: `{events: [...]}`
- Public endpoint

**GET /api/winners**
- Query: `event_id` (optional), `limit` (optional)
- Returns: `{weeks: [...]}`
- Public endpoint (returns weeks with published winners)

**GET /api/week-rankings/:week_id**
- Returns: `{week: {...}, results: [...]}`
- Shows full ranking with all scores
- Public endpoint (uses service key for judge_scores access)

### Admin Endpoints

All admin endpoints require admin authentication.

**GET /admin/dashboard**
- Returns: Admin dashboard HTML

**GET /admin/api/students**
- Returns: `{students: [...]}`

**POST /admin/api/students**
- Body: `{full_name, grade, email, is_active}`
- Returns: Created student

**POST /admin/api/import-students**
- Body: FormData with CSV file
- Returns: `{message, imported_count, errors}`

**GET /admin/api/results/:week_id**
- Returns: `{results: [...]}`
- Aggregated scores by participant

**POST /admin/api/publish-winners/:week_id**
- Calculates positions and marks winners
- Returns: `{message, published_count}`

**POST /admin/api/unpublish-winners/:week_id**
- Clears positions and winner flags
- Returns: Success message

**GET /admin/api/week/:week_id/publish-status**
- Returns: `{is_published: boolean}`

### Judge Endpoints

**GET /judge/scoring**
- Returns: Judge scoring interface
- Requires: Judge permission

**GET /judge/api/assignments**
- Returns: `{assignments: [...]}`
- Shows weeks where user has judge permissions

**GET /judge/api/criteria**
- Query: `category` (judge type)
- Returns: `{criteria: [...]}`

**POST /judge/api/submit-score**
- Body: `{participant_id, judge_type, score, criteria_breakdown, comments}`
- Returns: Created/updated score

**GET /judge/api/my-scores**
- Query: `week_id` (optional)
- Returns: `{scores: [...]}`

---

## Judging System

### Overview

The judging system allows administrators to grant temporary scoring permissions to users without making them full admins. Each judge is assigned to specific weeks and has a specific role (overall, content, style & delivery, or language).

### Setup Process

**1. Grant Permission**
- Admin navigates to Judge Permissions page
- Selects event, session, week
- Enters judge email
- Selects judge type
- Clicks "Grant Permission"

**2. Judge Logs In**
- Judge uses their email/password
- System detects judge permissions
- Shows "My Scoring" link in navigation

**3. Judge Scores**
- Judge sees list of assigned weeks
- Selects a week
- Views all participants
- Scores each participant
- Can edit scores before week is published

**4. Admin Reviews**
- Admin navigates to Results page
- Selects week
- Views aggregated scores from all judges
- Verifies scoring is complete

**5. Publish Results**
- Admin clicks "Publish Results to Dashboard"
- System calculates total scores
- Assigns positions (1, 2, 3, ...)
- Top 3 marked as winners
- Results visible on public winners page

### Score Calculation

Each participant's total score is the sum of scores from all judge types:

```
Total = Overall + Content + Style & Delivery + Language
Maximum possible = 10 + 10 + 10 + 10 = 40 points
```

If a judge type hasn't scored a participant, their score is treated as 0 (or excluded from total, depending on requirements).

### Judging Criteria

**Overall Performance (10 points)**
- Single holistic assessment
- One criterion: Overall Performance

**Content (10 points)**
- Evaluates message quality
- One criterion: Content

**Style & Delivery (10 points)**
- Evaluates presentation skills
- One criterion: Style & Delivery

**Language (10 points)**
- Evaluates language usage
- One criterion: Language

### Permission Management

**Grant Permission:**
- Creates entry in judge_permissions table
- Sets is_active=true
- Records granting admin's email

**Revoke Permission:**
- Sets is_active=false
- Records revocation timestamp
- Records revoking admin's email
- Judge loses access immediately

**Reactivate Permission:**
- Sets is_active=true
- Clears revocation fields
- Judge regains access

### Scoring Interface

**For Judges:**
1. Login with email/password
2. Click "My Scoring" in navigation
3. See list of assigned weeks
4. Click on a week to view participants
5. For each participant:
   - Enter score for each criterion
   - Add optional comments
   - Save score
6. Status shows "Scored" or "Pending" per participant
7. Can edit scores anytime before publishing

**Validation:**
- Cannot exceed max score per criterion
- All criteria required for submission
- Total calculated automatically
- Scores saved with timestamp

---

## Deployment Guide

### Production Deployment Steps

**1. Prepare Supabase**

Create production Supabase project:
- Set up new project at supabase.com
- Run MASTER_SCHEMA.sql
- Configure authentication settings:
  - JWT expiry: 14400 seconds (4 hours)
  - Enable email confirmation if desired
  - Set up SMTP for email (optional)

**2. Environment Configuration**

Update `.env` for production:
```
FLASK_SECRET_KEY=generate-secure-random-key
FLASK_ENV=production

SUPABASE_URL=https://your-production-project.supabase.co
SUPABASE_KEY=your-production-anon-key
SUPABASE_SERVICE_KEY=your-production-service-key
```

**3. Python Setup**

```bash
# Use production WSGI server
pip install gunicorn

# Install all dependencies
pip install -r requirements.txt
```

**4. Run with Gunicorn**

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Configuration:
- `-w 4`: 4 worker processes
- `-b 0.0.0.0:8000`: Bind to all interfaces on port 8000
- `app:app`: app.py file, app variable

**5. Reverse Proxy (Nginx)**

Sample Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/Ver1/static;
    }
}
```

**6. SSL Certificate**

Use Let's Encrypt for free SSL:
```bash
sudo certbot --nginx -d your-domain.com
```

**7. Process Management**

Use systemd or supervisor to keep app running:

Sample systemd service (`/etc/systemd/system/dsstalk.service`):
```ini
[Unit]
Description=DSS Talk Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/Ver1
Environment="PATH=/path/to/Ver1/venv/bin"
ExecStart=/path/to/Ver1/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable dsstalk
sudo systemctl start dsstalk
```

### Security Checklist

- [ ] Change FLASK_SECRET_KEY to random value
- [ ] Set FLASK_ENV to production
- [ ] Never commit .env file
- [ ] Use HTTPS in production
- [ ] Keep SUPABASE_SERVICE_KEY secret
- [ ] Enable Supabase RLS policies
- [ ] Regular database backups
- [ ] Monitor logs for errors
- [ ] Update dependencies regularly

### Performance Optimization

**Database:**
- Indexes already created in schema
- Use connection pooling if high traffic
- Monitor query performance

**Static Files:**
- Serve via Nginx (faster than Flask)
- Enable gzip compression
- Cache static assets

**Application:**
- Use multiple Gunicorn workers
- Monitor memory usage
- Set up error tracking (Sentry, etc.)

---

## User Guide

### For Students/Regular Users

**Login**
1. Navigate to application URL
2. Select preferred language (English/Nepali)
3. Select event type
4. Enter email and password
5. Click Login

**View Dashboard**
- See recent activity for selected event
- For Extempore: View upcoming weeks
- For Debate/Presentation: View recent winners

**View Winners**
- Click "Winners" in navigation
- Filter by event if desired
- Click "View Rankings" on any week
- See detailed scores and positions

**Switch Language**
- Click language toggle in header
- Interface updates immediately
- Preference saved for next visit

**Switch Event**
- Use event dropdown in header
- Dashboard updates to show event-specific content

### For Judges

**Access Scoring Interface**
1. Login with email/password
2. If you have judge permissions, "My Scoring" appears in navigation
3. Click "My Scoring"

**Score Participants**
1. See list of weeks you're assigned to
2. Click on a week
3. For each participant:
   - Click "Score" button
   - Enter scores for each criterion
   - Add comments (optional)
   - Click "Save Score"
4. Status updates to "Scored" when complete
5. Can edit scores by clicking "Edit Score"

**View Your Scores**
- "My Scoring" link shows all your assignments
- Table shows which participants you've scored
- Edit anytime before week is published

---

## Admin Guide

### Initial Setup

**Create First Admin**
1. Sign up for an account normally
2. Go to Supabase → Authentication → Users
3. Copy your user UUID
4. In SQL Editor, run:
   ```sql
   INSERT INTO admins (user_id) VALUES ('your-uuid-here');
   ```
5. Logout and login again
6. "Admin Panel" now appears in navigation

### Student Management

**Add Individual Student**
1. Admin Panel → Students
2. Click "Add New Student"
3. Fill in details (name, grade, email)
4. Click "Create Student"

**Import via CSV**
1. Prepare CSV file:
   ```csv
   full_name,grade
   John Doe,11
   Jane Smith,12
   ```
2. Admin Panel → Students
3. Click "Import from CSV"
4. Select file
5. Review preview
6. Click "Import"
7. Check results for errors

**Edit Student**
1. Find student in list
2. Click "Edit"
3. Modify details
4. Click "Update"

**Deactivate Student**
1. Find student
2. Toggle "Active" status
3. Inactive students won't appear in selections

### Session Management

**Create Session**
1. Admin Panel → Sessions
2. Click "Add New Session"
3. Select event
4. Enter session number
5. Set start/end dates
6. Click "Create"

**Manage Sessions**
- Toggle active/inactive status
- Only active sessions appear for week creation
- Edit details as needed

### Week Management

**Create Week (Manual Selection)**
1. Admin Panel → Weeks
2. Click "Add New Week"
3. Select event and session
4. Enter week number and topic
5. Select "Manual" participant mode
6. Check boxes next to students to include
7. Click "Create Week"

**Create Week (Random Selection for Extempore)**
1. Admin Panel → Weeks
2. Click "Add New Week"
3. Select Extempore event and session
4. Enter week number and topic
5. Select "Random" participant mode
6. Set number of participants (e.g., 5)
7. Optionally select grade filter (11 or 12)
8. Check "Reset if insufficient" if desired
9. Click "Create Week"

System will:
- Find students who haven't spoken
- Randomly select required number
- Mark them as participants
- Update speaker status

**Add Participants to Existing Week**
1. View week details
2. Click "Add Participants"
3. Choose manual or random
4. Follow same process as creation

### Judge Management

**Grant Judge Permission**
1. Admin Panel → Judge Permissions
2. Select event, session, week
3. Enter judge email (must have account)
4. Select judge type:
   - Overall
   - Content
   - Style & Delivery
   - Language
5. Click "Grant Permission"

Judge now has access to score that week.

**Revoke Permission**
1. Find permission in list
2. Click "Revoke"
3. Judge loses access immediately
4. Scores already submitted remain

**Reactivate Permission**
1. Find revoked permission
2. Click "Reactivate"
3. Judge regains access

### Results Management

**View Results**
1. Admin Panel → Results
2. Select event and session
3. Select week
4. View aggregated scores table
5. See scores from each judge type
6. Check totals

**Publish Results**
1. Verify all judges have scored
2. Review totals look correct
3. Click "Publish Results to Dashboard"
4. System assigns positions
5. Top 3 marked as winners
6. Results visible on public winners page

**Unpublish Results**
1. View published week
2. Click "Unpublish Results" button
3. Positions cleared
4. Winner flags removed
5. No longer visible on winners page

Use unpublish if:
- Need to correct scores
- Judge missed a participant
- Want to remove from public view

### Audit Logs

**View Action History**
1. Admin Panel → Logs
2. See chronological list of all admin actions
3. Filter by action type or entity
4. Review who did what and when
5. See old and new values for changes

Actions logged:
- Student create/update/delete
- Session create/update
- Week create/update
- Permission grant/revoke
- Results publish/unpublish

---

## Troubleshooting

### Common Issues

**Cannot login / Invalid credentials**
- Verify email and password
- Check Supabase Auth dashboard for user
- Try password reset flow
- Check browser console for errors

**Admin panel not showing**
- Verify user_id in admins table
- Logout and login again
- Check browser console for authorization errors
- Verify SUPABASE_SERVICE_KEY is correct

**Judge cannot see scoring interface**
- Verify permission granted for correct email
- Check permission is active (not revoked)
- Ensure week_id is correct
- Judge must logout/login after permission grant

**Random selection not working**
- Check students exist in specified grade
- Verify students are active
- Check session_speaker_status table
- May need to reset session if all have spoken

**Scores showing as zero**
- Verify judge_scores entries exist
- Check events.py uses SUPABASE_SERVICE_KEY
- Verify RLS policies on judge_scores
- Check browser console for API errors

**CSV import failing**
- Verify file format exactly matches: `full_name,grade`
- Check for special characters
- Ensure UTF-8 encoding
- Look at error messages for specific issues

### Database Issues

**Tables not found**
- Verify MASTER_SCHEMA.sql was run completely
- Check Supabase SQL Editor for errors
- Ensure correct database selected

**RLS preventing access**
- Admin routes use SERVICE_KEY (bypasses RLS)
- Public routes use anon key (subject to RLS)
- Check policy definitions in schema

**Missing data**
- Verify default events inserted
- Check cascade deletes haven't removed data
- Review audit logs for deletions

### Frontend Issues

**Language not switching**
- Clear browser localStorage
- Check i18n.js loading
- Verify translations object populated

**Styling broken**
- Check styles.css loading
- Verify static file path correct
- Clear browser cache

**API calls failing**
- Check browser console for errors
- Verify auth token in localStorage
- Check network tab for response details
- Confirm API endpoint paths

### Server Issues

**Application won't start**
- Check .env file exists and populated
- Verify all environment variables set
- Check Python version (3.8+)
- Review terminal for error messages

**Slow performance**
- Check database indexes exist
- Monitor Gunicorn worker count
- Review query efficiency
- Check Supabase plan limits

**Authentication errors**
- Verify Supabase URL and keys
- Check token expiration settings
- Review Supabase Auth dashboard

### Getting Help

If issues persist:
1. Check browser console (F12)
2. Review application terminal output
3. Check Supabase logs
4. Verify environment configuration
5. Test with fresh database

For critical issues:
- Export database backup
- Document steps to reproduce
- Gather error messages
- Check audit logs for clues

---

## Appendix

### Environment Variables Reference

```
FLASK_SECRET_KEY       # Random secret for Flask sessions
FLASK_ENV              # development or production
SUPABASE_URL          # Your Supabase project URL
SUPABASE_KEY          # Anon/public key
SUPABASE_SERVICE_KEY  # Service role key (keep secret)
```

### File Locations

- **Database Schema**: `database/MASTER_SCHEMA.sql`
- **Environment Template**: `.env.example`
- **Dependencies**: `requirements.txt`
- **Application Entry**: `app.py`
- **Routes**: `routes/*.py`
- **Templates**: `templates/**/*.html`
- **Static Assets**: `static/**/*`

### Important URLs

- Supabase Dashboard: https://app.supabase.com
- Authentication Management: Dashboard → Authentication
- SQL Editor: Dashboard → SQL Editor
- Database: Dashboard → Database

### Useful SQL Queries

**List all admins:**
```sql
SELECT a.id, a.user_id, u.email
FROM admins a
JOIN auth.users u ON a.user_id = u.id;
```

**Check judge permissions:**
```sql
SELECT jp.*, w.topic, u.email
FROM judge_permissions jp
JOIN weeks w ON jp.week_id = w.id
LEFT JOIN auth.users u ON jp.user_id = u.id
WHERE jp.is_active = true;
```

**View published weeks:**
```sql
SELECT w.*, COUNT(p.id) as winner_count
FROM weeks w
JOIN participants p ON w.id = p.week_id
WHERE p.is_winner = true
GROUP BY w.id;
```

**Reset session speakers:**
```sql
UPDATE session_speaker_status
SET has_spoken = false, spoken_in_week_id = null
WHERE session_id = 'session-uuid-here';
```

### Version History

- **v1.0** - Initial release with basic event management
- **v1.1** - Added judging system and permissions
- **v1.2** - Implemented results publishing and rankings
- **v1.3** - Updated criteria to 10 points per judge type
- **Current** - Complete system with all features

---

**Last Updated:** February 15, 2026

**System Status:** Production Ready

**Documentation Version:** 1.0
