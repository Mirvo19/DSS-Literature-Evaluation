// code

class AdminPanel {
    constructor() {
        this.events = [];
        this.sessions = [];
        this.students = [];
        this.judges = [];
        this.criteria = [];
    }
    
    async initialize() {
        // code
        const isAdmin = await requireAdmin();
        if (!isAdmin) return;
        
        updateUIForAuth();
        
        // code
        await this.loadEvents();
    }
    
    async loadEvents() {
        try {
            const response = await fetch('/api/events');
            const data = await response.json();
            this.events = data.events;
        } catch (error) {
            console.error('Failed to load events:', error);
        }
    }
    
    // code
    
    async loadStudents() {
        try {
            const response = await fetch('/admin/api/students', {
                headers: auth.getAuthHeaders()
            });
            
            if (!response.ok) throw new Error('Failed to load students');
            
            const data = await response.json();
            this.students = data.students;
            return this.students;
        } catch (error) {
            console.error('Error loading students:', error);
            throw error;
        }
    }
    
    async createStudent(studentData) {
        try {
            const response = await fetch('/admin/api/students', {
                method: 'POST',
                headers: auth.getAuthHeaders(),
                body: JSON.stringify(studentData)
            });
            
            if (!response.ok) throw new Error('Failed to create student');
            
            const data = await response.json();
            return data.student;
        } catch (error) {
            console.error('Error creating student:', error);
            throw error;
        }
    }
    
    async updateStudent(studentId, studentData) {
        try {
            const response = await fetch(`/admin/api/students/${studentId}`, {
                method: 'PUT',
                headers: auth.getAuthHeaders(),
                body: JSON.stringify(studentData)
            });
            
            if (!response.ok) throw new Error('Failed to update student');
            
            const data = await response.json();
            return data.student;
        } catch (error) {
            console.error('Error updating student:', error);
            throw error;
        }
    }
    
    async deleteStudent(studentId) {
        try {
            const response = await fetch(`/admin/api/students/${studentId}`, {
                method: 'DELETE',
                headers: auth.getAuthHeaders()
            });
            
            if (!response.ok) throw new Error('Failed to delete student');
            
            return true;
        } catch (error) {
            console.error('Error deleting student:', error);
            throw error;
        }
    }
    
    async importCSV(csvContent) {
        try {
            const response = await fetch('/admin/api/import-csv', {
                method: 'POST',
                headers: auth.getAuthHeaders(),
                body: JSON.stringify({ csv_content: csvContent })
            });
            
            if (!response.ok) throw new Error('Failed to import CSV');
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error importing CSV:', error);
            throw error;
        }
    }
    
    // code
    
    async loadSessions() {
        try {
            const response = await fetch('/admin/api/sessions', {
                headers: auth.getAuthHeaders()
            });
            
            if (!response.ok) throw new Error('Failed to load sessions');
            
            const data = await response.json();
            this.sessions = data.sessions;
            return this.sessions;
        } catch (error) {
            console.error('Error loading sessions:', error);
            throw error;
        }
    }
    
    async createSession(sessionData) {
        try {
            const response = await fetch('/admin/api/sessions', {
                method: 'POST',
                headers: auth.getAuthHeaders(),
                body: JSON.stringify(sessionData)
            });
            
            if (!response.ok) throw new Error('Failed to create session');
            
            const data = await response.json();
            return data.session;
        } catch (error) {
            console.error('Error creating session:', error);
            throw error;
        }
    }
    
    async updateSession(sessionId, sessionData) {
        try {
            const response = await fetch(`/admin/api/sessions/${sessionId}`, {
                method: 'PUT',
                headers: auth.getAuthHeaders(),
                body: JSON.stringify(sessionData)
            });
            
            if (!response.ok) throw new Error('Failed to update session');
            
            const data = await response.json();
            return data.session;
        } catch (error) {
            console.error('Error updating session:', error);
            throw error;
        }
    }
    
    async deleteSession(sessionId) {
        try {
            const response = await fetch(`/admin/api/sessions/${sessionId}`, {
                method: 'DELETE',
                headers: auth.getAuthHeaders()
            });
            
            if (!response.ok) throw new Error('Failed to delete session');
            
            return true;
        } catch (error) {
            console.error('Error deleting session:', error);
            throw error;
        }
    }
    
    async resetSessionSpeakers(sessionId) {
        try {
            const response = await fetch(`/admin/api/sessions/${sessionId}/reset-speakers`, {
                method: 'POST',
                headers: auth.getAuthHeaders()
            });
            
            if (!response.ok) throw new Error('Failed to reset speakers');
            
            return true;
        } catch (error) {
            console.error('Error resetting speakers:', error);
            throw error;
        }
    }
    
    // code
    
    async loadWeeks() {
        try {
            const response = await fetch('/admin/api/weeks', {
                headers: auth.getAuthHeaders()
            });
            
            if (!response.ok) throw new Error('Failed to load weeks');
            
            const data = await response.json();
            return data.weeks;
        } catch (error) {
            console.error('Error loading weeks:', error);
            throw error;
        }
    }
    
    async createWeek(weekData) {
        try {
            const response = await fetch('/admin/api/weeks', {
                method: 'POST',
                headers: auth.getAuthHeaders(),
                body: JSON.stringify(weekData)
            });
            
            if (!response.ok) throw new Error('Failed to create week');
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error creating week:', error);
            throw error;
        }
    }
    
    async updateWeek(weekId, weekData) {
        try {
            const response = await fetch(`/admin/api/weeks/${weekId}`, {
                method: 'PUT',
                headers: auth.getAuthHeaders(),
                body: JSON.stringify(weekData)
            });
            
            if (!response.ok) throw new Error('Failed to update week');
            
            const data = await response.json();
            return data.week;
        } catch (error) {
            console.error('Error updating week:', error);
            throw error;
        }
    }
    
    async deleteWeek(weekId) {
        try {
            const response = await fetch(`/admin/api/weeks/${weekId}`, {
                method: 'DELETE',
                headers: auth.getAuthHeaders()
            });
            
            if (!response.ok) throw new Error('Failed to delete week');
            
            return true;
        } catch (error) {
            console.error('Error deleting week:', error);
            throw error;
        }
    }
    
    // code
    
    async updateParticipant(participantId, participantData) {
        try {
            const response = await fetch(`/admin/api/participants/${participantId}`, {
                method: 'PUT',
                headers: auth.getAuthHeaders(),
                body: JSON.stringify(participantData)
            });
            
            if (!response.ok) throw new Error('Failed to update participant');
            
            const data = await response.json();
            return data.participant;
        } catch (error) {
            console.error('Error updating participant:', error);
            throw error;
        }
    }
    
    async addParticipant(participantData) {
        try {
            const response = await fetch('/admin/api/participants', {
                method: 'POST',
                headers: auth.getAuthHeaders(),
                body: JSON.stringify(participantData)
            });
            
            if (!response.ok) throw new Error('Failed to add participant');
            
            const data = await response.json();
            return data.participant;
        } catch (error) {
            console.error('Error adding participant:', error);
            throw error;
        }
    }
    
    async removeParticipant(participantId) {
        try {
            const response = await fetch(`/admin/api/participants/${participantId}`, {
                method: 'DELETE',
                headers: auth.getAuthHeaders()
            });
            
            if (!response.ok) throw new Error('Failed to remove participant');
            
            return true;
        } catch (error) {
            console.error('Error removing participant:', error);
            throw error;
        }
    }
    
    // code
    
    async loadJudges() {
        try {
            const response = await fetch('/admin/api/judges', {
                headers: auth.getAuthHeaders()
            });
            
            if (!response.ok) throw new Error('Failed to load judges');
            
            const data = await response.json();
            this.judges = data.judges;
            return this.judges;
        } catch (error) {
            console.error('Error loading judges:', error);
            throw error;
        }
    }
    
    async createJudge(judgeData) {
        try {
            const response = await fetch('/admin/api/judges', {
                method: 'POST',
                headers: auth.getAuthHeaders(),
                body: JSON.stringify(judgeData)
            });
            
            if (!response.ok) throw new Error('Failed to create judge');
            
            const data = await response.json();
            return data.judge;
        } catch (error) {
            console.error('Error creating judge:', error);
            throw error;
        }
    }
    
    // code
    
    async loadCriteria() {
        try {
            const response = await fetch('/admin/api/judging-criteria', {
                headers: auth.getAuthHeaders()
            });
            
            if (!response.ok) throw new Error('Failed to load criteria');
            
            const data = await response.json();
            this.criteria = data.criteria;
            return this.criteria;
        } catch (error) {
            console.error('Error loading criteria:', error);
            throw error;
        }
    }
}

// code
const adminPanel = new AdminPanel();

// code
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('hidden');
    }
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('hidden');
    }
}

function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '10000';
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// code
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { adminPanel, showModal, hideModal, showLoading, hideLoading, showAlert };
}
