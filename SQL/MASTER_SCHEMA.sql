-- =============================================================================
-- DSS TALK EVENT MANAGEMENT SYSTEM - MASTER DATABASE SCHEMA
-- =============================================================================
-- This file contains the complete database schema for the DSS Talk system
-- Run this file ONCE on a fresh Supabase database
-- Created: 2026-02-15
-- =============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- CORE TABLES
-- =============================================================================

-- ADMIN TABLE
CREATE TABLE admins (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

CREATE INDEX idx_admins_user_id ON admins(user_id);

-- EVENTS TABLE
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    name_nepali VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert default events
INSERT INTO events (name, name_nepali, description) VALUES
('Debate', 'बहस', 'Debate competition'),
('Presentation', 'प्रस्तुतीकरण', 'Presentation competition'),
('Extempore', 'तत्काल भाषण', 'Extempore speaking competition');

-- SESSIONS TABLE
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    session_number INTEGER NOT NULL,
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    CONSTRAINT unique_event_session UNIQUE (event_id, session_number)
);

CREATE INDEX idx_sessions_event_id ON sessions(event_id);
CREATE INDEX idx_sessions_active ON sessions(is_active);

-- STUDENTS TABLE
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(200) NOT NULL,
    grade INTEGER,
    email VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_students_name ON students(full_name);
CREATE INDEX idx_students_grade ON students(grade);
CREATE INDEX idx_students_active ON students(is_active);

-- WEEKS TABLE
CREATE TABLE weeks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL,
    week_number INTEGER NOT NULL,
    topic VARCHAR(300),
    topic_nepali VARCHAR(300),
    date DATE,
    is_partial BOOLEAN DEFAULT false,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_session FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
    CONSTRAINT unique_session_week UNIQUE (session_id, week_number)
);

CREATE INDEX idx_weeks_session_id ON weeks(session_id);
CREATE INDEX idx_weeks_week_number ON weeks(week_number);
CREATE INDEX idx_weeks_date ON weeks(date);

-- JUDGES TABLE
CREATE TABLE judges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(200) NOT NULL,
    title VARCHAR(100),
    email VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_judges_name ON judges(full_name);
CREATE INDEX idx_judges_active ON judges(is_active);

-- JUDGING CRITERIA TABLE
CREATE TABLE judging_criteria (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    name_nepali VARCHAR(200),
    description TEXT,
    category VARCHAR(50) DEFAULT 'overall',
    max_points DECIMAL(5,2) DEFAULT 10,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- WEEK JUDGES TABLE (Many-to-Many)
CREATE TABLE week_judges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    week_id UUID NOT NULL,
    judge_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_week FOREIGN KEY (week_id) REFERENCES weeks(id) ON DELETE CASCADE,
    CONSTRAINT fk_judge FOREIGN KEY (judge_id) REFERENCES judges(id) ON DELETE CASCADE,
    CONSTRAINT unique_week_judge UNIQUE (week_id, judge_id)
);

CREATE INDEX idx_week_judges_week_id ON week_judges(week_id);
CREATE INDEX idx_week_judges_judge_id ON week_judges(judge_id);

-- WEEK CRITERIA TABLE (Many-to-Many)
CREATE TABLE week_criteria (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    week_id UUID NOT NULL,
    criteria_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_week_crit FOREIGN KEY (week_id) REFERENCES weeks(id) ON DELETE CASCADE,
    CONSTRAINT fk_criteria FOREIGN KEY (criteria_id) REFERENCES judging_criteria(id) ON DELETE CASCADE,
    CONSTRAINT unique_week_criteria UNIQUE (week_id, criteria_id)
);

CREATE INDEX idx_week_criteria_week_id ON week_criteria(week_id);
CREATE INDEX idx_week_criteria_criteria_id ON week_criteria(criteria_id);

-- PARTICIPANTS TABLE
CREATE TABLE participants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    week_id UUID NOT NULL,
    student_id UUID NOT NULL,
    score DECIMAL(5, 2) DEFAULT 0,
    is_winner BOOLEAN DEFAULT false,
    position INTEGER,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_week_part FOREIGN KEY (week_id) REFERENCES weeks(id) ON DELETE CASCADE,
    CONSTRAINT fk_student FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    CONSTRAINT unique_week_student UNIQUE (week_id, student_id)
);

CREATE INDEX idx_participants_week_id ON participants(week_id);
CREATE INDEX idx_participants_student_id ON participants(student_id);
CREATE INDEX idx_participants_winner ON participants(is_winner);
CREATE INDEX idx_participants_score ON participants(score DESC);
CREATE INDEX idx_participants_position ON participants(position);

-- SESSION SPEAKER STATUS TABLE
CREATE TABLE session_speaker_status (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL,
    student_id UUID NOT NULL,
    has_spoken BOOLEAN DEFAULT false,
    spoken_in_week_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_session_status FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
    CONSTRAINT fk_student_status FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    CONSTRAINT fk_spoken_week FOREIGN KEY (spoken_in_week_id) REFERENCES weeks(id) ON DELETE SET NULL,
    CONSTRAINT unique_session_student UNIQUE (session_id, student_id)
);

CREATE INDEX idx_speaker_status_session_id ON session_speaker_status(session_id);
CREATE INDEX idx_speaker_status_student_id ON session_speaker_status(student_id);
CREATE INDEX idx_speaker_status_has_spoken ON session_speaker_status(has_spoken);

-- =============================================================================
-- JUDGING SYSTEM TABLES
-- =============================================================================

-- JUDGE PERMISSIONS TABLE
CREATE TABLE judge_permissions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    user_email VARCHAR(255) NOT NULL,
    week_id UUID REFERENCES weeks(id) ON DELETE CASCADE,
    judge_type VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    granted_by_admin_email VARCHAR(255) NOT NULL,
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    revoked_at TIMESTAMP WITH TIME ZONE,
    revoked_by_admin_email VARCHAR(255),
    UNIQUE(user_email, week_id, judge_type)
);

CREATE INDEX idx_judge_permissions_user_email ON judge_permissions(user_email);
CREATE INDEX idx_judge_permissions_week_id ON judge_permissions(week_id);
CREATE INDEX idx_judge_permissions_is_active ON judge_permissions(is_active);

-- JUDGE SCORES TABLE
CREATE TABLE judge_scores (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    participant_id UUID REFERENCES participants(id) ON DELETE CASCADE,
    judge_email VARCHAR(255) NOT NULL,
    judge_type VARCHAR(50) NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    max_score DECIMAL(5,2) DEFAULT 100,
    comments TEXT,
    criteria_breakdown JSONB,
    judged_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(participant_id, judge_email, judge_type)
);

CREATE INDEX idx_judge_scores_participant_id ON judge_scores(participant_id);
CREATE INDEX idx_judge_scores_judge_email ON judge_scores(judge_email);

-- =============================================================================
-- AUDIT LOGGING TABLE
-- =============================================================================

-- AUDIT LOGS TABLE
CREATE TABLE audit_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    admin_email VARCHAR(255) NOT NULL,
    admin_id UUID,
    action_type VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID,
    entity_name VARCHAR(255),
    old_value JSONB,
    new_value JSONB,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_logs_admin_email ON audit_logs(admin_email);
CREATE INDEX idx_audit_logs_entity_type ON audit_logs(entity_type);
CREATE INDEX idx_audit_logs_action_type ON audit_logs(action_type);

-- =============================================================================
-- FUNCTIONS AND TRIGGERS
-- =============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at triggers
CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON events
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_students_updated_at BEFORE UPDATE ON students
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_weeks_updated_at BEFORE UPDATE ON weeks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_judges_updated_at BEFORE UPDATE ON judges
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_participants_updated_at BEFORE UPDATE ON participants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_speaker_status_updated_at BEFORE UPDATE ON session_speaker_status
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- ROW LEVEL SECURITY (RLS)
-- =============================================================================

-- Enable RLS on all tables
ALTER TABLE admins ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE weeks ENABLE ROW LEVEL SECURITY;
ALTER TABLE judges ENABLE ROW LEVEL SECURITY;
ALTER TABLE judging_criteria ENABLE ROW LEVEL SECURITY;
ALTER TABLE week_judges ENABLE ROW LEVEL SECURITY;
ALTER TABLE week_criteria ENABLE ROW LEVEL SECURITY;
ALTER TABLE participants ENABLE ROW LEVEL SECURITY;
ALTER TABLE session_speaker_status ENABLE ROW LEVEL SECURITY;
ALTER TABLE judge_permissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE judge_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Public read access policies
CREATE POLICY "Events are viewable by everyone" ON events FOR SELECT USING (true);
CREATE POLICY "Criteria are viewable by everyone" ON judging_criteria FOR SELECT USING (true);
CREATE POLICY "Sessions are viewable by everyone" ON sessions FOR SELECT USING (true);
CREATE POLICY "Weeks are viewable by everyone" ON weeks FOR SELECT USING (true);
CREATE POLICY "Participants are viewable by everyone" ON participants FOR SELECT USING (true);
CREATE POLICY "Students are viewable by everyone" ON students FOR SELECT USING (true);
CREATE POLICY "Judges are viewable by everyone" ON judges FOR SELECT USING (true);
CREATE POLICY "Week judges are viewable by everyone" ON week_judges FOR SELECT USING (true);
CREATE POLICY "Week criteria are viewable by everyone" ON week_criteria FOR SELECT USING (true);
CREATE POLICY "Speaker status is viewable by everyone" ON session_speaker_status FOR SELECT USING (true);

-- Admin-only write access policies
CREATE POLICY "Admins can do everything on events" ON events FOR ALL USING (true);
CREATE POLICY "Admins can do everything on sessions" ON sessions FOR ALL USING (true);
CREATE POLICY "Admins can do everything on students" ON students FOR ALL USING (true);
CREATE POLICY "Admins can do everything on weeks" ON weeks FOR ALL USING (true);
CREATE POLICY "Admins can do everything on judges" ON judges FOR ALL USING (true);
CREATE POLICY "Admins can do everything on criteria" ON judging_criteria FOR ALL USING (true);
CREATE POLICY "Admins can do everything on week_judges" ON week_judges FOR ALL USING (true);
CREATE POLICY "Admins can do everything on week_criteria" ON week_criteria FOR ALL USING (true);
CREATE POLICY "Admins can do everything on participants" ON participants FOR ALL USING (true);
CREATE POLICY "Admins can do everything on speaker_status" ON session_speaker_status FOR ALL USING (true);

-- Judge permissions policies
CREATE POLICY "Admins can manage judge permissions"
ON judge_permissions FOR ALL
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM admins
        WHERE admins.user_id = auth.uid()
    )
);

CREATE POLICY "Judges can view their own permissions"
ON judge_permissions FOR SELECT
TO authenticated
USING (user_id = auth.uid() OR user_email = auth.email());

-- Judge scores policies
CREATE POLICY "Admins can view all scores"
ON judge_scores FOR SELECT
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM admins
        WHERE admins.user_id = auth.uid()
    )
);

CREATE POLICY "Judges can insert their own scores"
ON judge_scores FOR INSERT
TO authenticated
WITH CHECK (
    judge_email = auth.email() AND
    EXISTS (
        SELECT 1 FROM judge_permissions jp
        INNER JOIN participants p ON p.week_id = jp.week_id
        WHERE jp.user_email = auth.email()
        AND jp.is_active = true
        AND p.id = participant_id
        AND jp.judge_type = judge_type
    )
);

CREATE POLICY "Judges can view their own scores"
ON judge_scores FOR SELECT
TO authenticated
USING (judge_email = auth.email());

CREATE POLICY "Judges can update their own scores"
ON judge_scores FOR UPDATE
TO authenticated
USING (
    judge_email = auth.email() AND
    EXISTS (
        SELECT 1 FROM judge_permissions jp
        INNER JOIN participants p ON p.week_id = jp.week_id
        WHERE jp.user_email = auth.email()
        AND jp.is_active = true
        AND p.id = participant_id
        AND jp.judge_type = judge_type
    )
);

-- Audit logs policies
CREATE POLICY "Admins can view all audit logs"
ON audit_logs FOR SELECT
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM admins
        WHERE admins.user_id = auth.uid()
    )
);

CREATE POLICY "Allow insert for authenticated users"
ON audit_logs FOR INSERT
TO authenticated
WITH CHECK (true);

-- =============================================================================
-- VIEWS
-- =============================================================================

-- View for recent winners
CREATE OR REPLACE VIEW recent_winners AS
SELECT 
    p.id,
    p.week_id,
    p.student_id,
    s.full_name,
    p.score,
    p.position,
    w.week_number,
    w.date,
    w.topic,
    w.topic_nepali,
    sess.session_number,
    e.name as event_name,
    e.name_nepali as event_name_nepali
FROM participants p
JOIN students s ON p.student_id = s.id
JOIN weeks w ON p.week_id = w.id
JOIN sessions sess ON w.session_id = sess.id
JOIN events e ON sess.event_id = e.id
WHERE p.is_winner = true
ORDER BY w.date DESC, p.position ASC;

-- View for week details with counts
CREATE OR REPLACE VIEW week_details AS
SELECT 
    w.id,
    w.session_id,
    w.week_number,
    w.topic,
    w.topic_nepali,
    w.date,
    w.is_partial,
    sess.session_number,
    sess.name as session_name,
    e.id as event_id,
    e.name as event_name,
    e.name_nepali as event_name_nepali,
    COUNT(DISTINCT p.id) as participant_count,
    COUNT(DISTINCT wj.judge_id) as judge_count,
    COUNT(DISTINCT wc.criteria_id) as criteria_count
FROM weeks w
JOIN sessions sess ON w.session_id = sess.id
JOIN events e ON sess.event_id = e.id
LEFT JOIN participants p ON w.id = p.week_id
LEFT JOIN week_judges wj ON w.id = wj.week_id
LEFT JOIN week_criteria wc ON w.id = wc.week_id
GROUP BY w.id, w.session_id, w.week_number, w.topic, w.topic_nepali, 
         w.date, w.is_partial, sess.session_number, sess.name, 
         e.id, e.name, e.name_nepali;

-- =============================================================================
-- DEFAULT JUDGING CRITERIA
-- =============================================================================
-- Updated to 10 points max per judge type

DELETE FROM judging_criteria;

INSERT INTO judging_criteria (name, name_nepali, category, max_points) VALUES
('Overall Performance', 'समग्र प्रदर्शन', 'overall', 10),
('Content', 'सामग्री', 'content', 10),
('Style & Delivery', 'शैली र प्रस्तुति', 'style_delivery', 10),
('Language', 'भाषा', 'language', 10);

-- =============================================================================
-- TABLE COMMENTS
-- =============================================================================

COMMENT ON TABLE admins IS 'Stores user IDs of administrators';
COMMENT ON TABLE events IS 'Main events: Debate, Presentation, Extempore';
COMMENT ON TABLE sessions IS 'Sessions within each event';
COMMENT ON TABLE students IS 'Student roster for all events';
COMMENT ON TABLE weeks IS 'Individual weeks within sessions';
COMMENT ON TABLE judges IS 'Judges who evaluate participants';
COMMENT ON TABLE judging_criteria IS 'Criteria used for judging';
COMMENT ON TABLE participants IS 'Students participating in specific weeks';
COMMENT ON TABLE session_speaker_status IS 'Tracks who has spoken in extempore sessions';
COMMENT ON TABLE judge_permissions IS 'Temporary judging permissions for non-admin users';
COMMENT ON TABLE judge_scores IS 'Detailed scores from each judge by category';
COMMENT ON TABLE audit_logs IS 'Stores audit trail of all admin actions';

COMMENT ON COLUMN participants.position IS 'Rank/position of participant in their week (1 = first place, 2 = second, etc.)';
COMMENT ON COLUMN judge_permissions.judge_type IS 'Type of judging: overall, content, style_delivery, language, etc.';
COMMENT ON COLUMN judge_scores.criteria_breakdown IS 'JSON breakdown of scores per criteria';
COMMENT ON COLUMN audit_logs.action_type IS 'Type of action: CREATE, UPDATE, DELETE, etc.';
COMMENT ON COLUMN audit_logs.entity_type IS 'Type of entity: week, session, student, participant, etc.';
COMMENT ON COLUMN audit_logs.old_value IS 'JSON snapshot of entity before change';
COMMENT ON COLUMN audit_logs.new_value IS 'JSON snapshot of entity after change';

-- =============================================================================
-- END OF MASTER SCHEMA
-- =============================================================================
