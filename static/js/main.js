// main app

class App {
    constructor() {
        this.selectedEvent = localStorage.getItem('selected_event') || 'debate';
        this.selectedGrade = localStorage.getItem('selected_grade') || '11';
        this.currentEventId = null;
        this.events = [];
    }
    
    async initialize() {
        // check auth
        const authenticated = await requireAuth();
        if (!authenticated) return;
        
        // load events
        await this.loadEvents();
        
        // setup header
        this.updateHeader();
        updateUIForAuth();
        
        // load content
        await this.loadContent();
    }
    
    async loadEvents() {
        try {
            const response = await fetch('/api/events');
            const data = await response.json();
            this.events = data.events;
            
            // find current event
            const currentEvent = this.events.find(e => 
                e.name.toLowerCase() === this.selectedEvent.toLowerCase()
            );
            
            if (currentEvent) {
                this.currentEventId = currentEvent.id;
            }
        } catch (error) {
            console.error('Failed to load events:', error);
        }
    }
    
    updateHeader() {
        const eventSelect = document.getElementById('eventSelect');
        if (eventSelect) {
            eventSelect.value = this.selectedEvent;
            
            eventSelect.addEventListener('change', async (e) => {
                this.selectedEvent = e.target.value;
                localStorage.setItem('selected_event', this.selectedEvent);
                
                // reload on change
                await this.loadEvents();
                await this.loadContent();
            });
        }
        
        // logout button
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', async () => {
                await auth.logout();
                window.location.href = '/';
            });
        }
    }
    
    async loadContent() {
        const contentArea = document.getElementById('contentArea');
        if (!contentArea) return;
        
        // show loading
        contentArea.innerHTML = '<div class="spinner"></div>';
        
        if (this.selectedEvent === 'extempore') {
            await this.loadExtemporeWeeks();
        } else {
            await this.loadRecentWinners();
        }
    }
    
    async loadExtemporeWeeks() {
        const contentArea = document.getElementById('contentArea');
        
        try {
            const lang = window.APP_LANG || i18n.getLanguage();
            const response = await fetch(`/api/weeks-by-event/${this.currentEventId}?lang=${lang}`, {
                headers: auth.getAuthHeaders()
            });
            
            const data = await response.json();
            
            if (data.weeks && data.weeks.length > 0) {
                contentArea.innerHTML = `
                    <h2 data-i18n="weeks">${i18n.t('weeks')}</h2>
                    <div class="week-list">
                        ${data.weeks.map(week => `
                            <div class="week-item" onclick="window.location.href='/${window.APP_LANG}/week/${week.id}'">
                                <div class="week-number">
                                    ${i18n.t('session')} ${week.sessions.session_number} - ${i18n.t('week')} ${week.week_number}
                                </div>
                                <div class="week-topic">
                                    ${i18n.getLanguage() === 'ne' && week.topic_nepali ? week.topic_nepali : week.topic || ''}
                                </div>
                                <div class="week-date">
                                    ${week.date ? new Date(week.date).toLocaleDateString() : ''}
                                    ${week.is_partial ? `<span class="badge badge-warning">${i18n.t('partialWeek')}</span>` : ''}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `;
            } else {
                contentArea.innerHTML = `
                    <div class="card text-center">
                        <p data-i18n="noData">${i18n.t('noData')}</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Failed to load weeks:', error);
            contentArea.innerHTML = `
                <div class="alert alert-error">${i18n.t('error')}: ${error.message}</div>
            `;
        }
    }
    
    async loadRecentWinners() {
        const contentArea = document.getElementById('contentArea');
        
        try {
            console.log('Loading winners for event:', this.currentEventId);
            
            const url = this.currentEventId 
                ? `/api/winners?event_id=${this.currentEventId}`
                : '/api/winners';
                
            const response = await fetch(url);
            
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                const text = await response.text();
                console.error('Error response:', text);
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            if (data.weeks && data.weeks.length > 0) {
                contentArea.innerHTML = `
                    <h2 data-i18n="recentWinners">${i18n.t('recentWinners')}</h2>
                    <div class="table-container">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th data-i18n="eventName">${i18n.t('eventName')}</th>
                                    <th data-i18n="weekNumber">${i18n.t('weekNumber')}</th>
                                    <th>Topic</th>
                                    <th data-i18n="date">${i18n.t('date')}</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.weeks.map(week => {
                                    const eventName = i18n.getLanguage() === 'ne' && week.sessions?.events?.name_nepali
                                        ? week.sessions.events.name_nepali
                                        : week.sessions?.events?.name || '-';
                                    
                                    const topic = i18n.getLanguage() === 'ne' && week.topic_nepali
                                        ? week.topic_nepali
                                        : week.topic || '-';
                                    
                                    return `
                                        <tr>
                                            <td><strong>${eventName}</strong></td>
                                            <td>${i18n.t('week')} ${week.week_number}</td>
                                            <td>${topic}</td>
                                            <td>${week.date ? new Date(week.date).toLocaleDateString() : '-'}</td>
                                            <td>
                                                <a href="/${window.APP_LANG}/week-rankings/${week.id}" class="btn btn-sm btn-primary">
                                                    View Rankings
                                                </a>
                                            </td>
                                        </tr>
                                    `;
                                }).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            } else {
                contentArea.innerHTML = `
                    <div class="card text-center">
                        <h2 data-i18n="recentWinners">${i18n.t('recentWinners')}</h2>
                        <p data-i18n="noData">${i18n.t('noData')}</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Failed to load winners:', error);
            contentArea.innerHTML = `
                <div class="alert alert-error">${i18n.t('error')}: ${error.message}</div>
            `;
        }
    }
}

// boot the app
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', async () => {
        const app = new App();
        await app.initialize();
        i18n.updatePageTexts();
    });
}
