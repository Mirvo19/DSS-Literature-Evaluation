# DSS Talk Event Management System

A full-stack web application for managing school speaking events including Debate, Presentation, and Extempore competitions. Features bilingual support (English/Nepali) and a comprehensive administrative control panel.

## Features

- **Authentication**: Secure login and signup via Supabase
- **Bilingual Interface**: Full English and Nepali language support
- **Event Management**: Support for Debate, Presentation, and Extempore events
- **Random Selection**: Intelligent participant selection algorithm for Extempore
- **Winners Tracking**: Complete tracking and display of competition results
- **Admin CMS**: Full content management system for administrators
- **CSV Import**: Bulk student import functionality
- **Judge System**: Temporary permissions with role-based scoring
- **Results Publishing**: Position-based ranking with publish/unpublish controls

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database & Auth**: Supabase (PostgreSQL + Auth)

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Supabase account
- pip (Python package manager)

### 2. Supabase Setup

1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. Run the complete SQL schema from `database/MASTER_SCHEMA.sql` in the Supabase SQL editor
3. Configure JWT expiry to 14400 seconds (4 hours) in Authentication settings
4. Copy your project URL and API keys (anon key and service role key)

### 3. Local Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your Supabase credentials

6. Run the application:
   ```bash
   python app.py
   ```

7. Open browser to `http://localhost:5000`

## Admin Setup

To grant admin access to a user:

1. Sign up a user account normally
2. Get the user's UUID from Supabase Auth dashboard
3. Run this SQL in Supabase SQL editor:
   ```sql
   INSERT INTO admins (user_id) VALUES ('user-uuid-here');
   ```

## Project Structure

```
Ver1/
├── app.py                 # Flask application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── MASTER.md             # Complete system documentation
├── database/
│   └── MASTER_SCHEMA.sql # Complete database schema
├── routes/
│   ├── auth.py           # Authentication routes
│   ├── events.py         # Public event routes
│   ├── admin.py          # Admin CMS routes
│   └── judge.py          # Judge scoring routes
├── utils/
│   ├── auth.py           # Authentication utilities
│   ├── csv_handler.py    # CSV import logic
│   ├── random_selector.py # Extempore selection logic
│   └── audit_logger.py   # Action logging utility
├── static/
│   ├── css/
│   │   └── styles.css    # Application styles
│   └── js/
│       ├── auth.js       # Authentication logic
│       ├── main.js       # Main application logic
│       ├── admin.js      # Admin panel logic
│       └── i18n.js       # Internationalization
└── templates/
    ├── login.html        # Login page
    ├── signup.html       # Signup page
    ├── dashboard.html    # User dashboard
    ├── winners.html      # Winners listing
    ├── week-rankings.html # Detailed rankings
    ├── admin/
    │   ├── dashboard.html # Admin dashboard
    │   ├── students.html  # Student management
    │   ├── sessions.html  # Session management
    │   ├── weeks.html     # Week management
    │   ├── results.html   # Results and publishing
    │   └── judge_permissions.html
    └── judge/
        └── scoring.html   # Judge scoring interface
```

## Usage Guide

### For Regular Users

1. **Login**: Select language and event, then login
2. **View Events**: Navigate weeks (Extempore) or winners (Debate)
3. **Week Details**: Click on any week to see participants, judges, and scores
4. **Switch Events**: Use header dropdown to switch between events
5. **Language Toggle**: Change language anytime from header

### For Administrators

1. **Access Admin Panel**: After login, click "Admin Panel" in header
2. **Manage Students**: Add individual students or import via CSV
3. **Create Sessions**: Organize events into competition sessions
4. **Create Weeks**: Add weeks with automated or manual participant selection
5. **Grant Judge Permissions**: Assign temporary judge access to users
6. **Review Results**: View aggregated scores from all judges
7. **Publish Winners**: Calculate positions and publish to public winners page

### For Judges

1. **Login**: Use your email and password
2. **My Scoring**: Access your assigned weeks
3. **Score Participants**: Enter scores for each participant based on your judge type
4. **Edit Scores**: Modify scores anytime before results are published

### CSV Import Format

```csv
full_name,grade
John Doe,11
Jane Smith,12
```

## Judging System

The application supports a multi-judge scoring system:

- **Judge Types**: Overall, Content, Style & Delivery, Language
- **Points**: 10 points maximum per judge type
- **Total Possible**: 40 points (10 from each judge type)
- **Permissions**: Temporary access granted per week by administrators
- **Publishing**: Administrators review scores and publish results with position rankings

## Extempore Selection Logic

The system intelligently selects participants for Extempore events:

1. Only selects students who haven't spoken in current session
2. Randomizes selection to ensure fairness
3. Tracks participation to avoid duplicates
4. Provides options when insufficient students:
   - Create partial week
   - Reset session and select from full pool
5. Allows manual override by admin

## Security Notes

- All admin routes are server-protected with authentication decorators
- Authentication uses Supabase Auth with JWT tokens
- Service keys are never exposed to frontend code
- Admin access requires manual database entry (not automatic)
- Row Level Security policies enforced at database level
- Judge permissions are temporary and revokable
- All admin actions logged in audit_logs table

## Documentation

For complete documentation including:
- Detailed setup instructions
- Database schema reference
- Complete API documentation
- Troubleshooting guide
- User and admin guides

See [MASTER.md](MASTER.md) for comprehensive documentation.

## License

MIT License - Free to use for educational purposes
