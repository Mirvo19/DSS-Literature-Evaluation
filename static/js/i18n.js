// i18n

const translations = {
    en: {
        // auth
        login: 'Login',
        signup: 'Sign Up',
        logout: 'Logout',
        email: 'Email',
        password: 'Password',
        confirmPassword: 'Confirm Password',
        loginButton: 'Login',
        signupButton: 'Sign Up',
        alreadyHaveAccount: 'Already have an account?',
        dontHaveAccount: "Don't have an account?",
        
        // nav
        dashboard: 'Dashboard',
        winners: 'Winners',
        adminPanel: 'Admin Panel',
        events: 'Events',
        
        // events
        debate: 'Debate',
        presentation: 'Presentation',
        extempore: 'Extempore',
        selectEvent: 'Select Event',
        selectLanguage: 'Select Language',
        selectGrade: 'Select Grade',
        
        // language
        english: 'English',
        nepali: 'Nepali',
        
        // grades
        grade11: 'Grade 11',
        grade12: 'Grade 12',
        
        // week details
        week: 'Week',
        session: 'Session',
        participants: 'Participants',
        judges: 'Judges',
        criteria: 'Judging Criteria',
        score: 'Score',
        winner: 'Winner',
        topic: 'Topic',
        date: 'Date',
        
        // winners
        recentWinners: 'Recent Winners',
        position: 'Position',
        studentName: 'Student Name',
        eventName: 'Event',
        weekNumber: 'Week',
        
        // admin
        adminDashboard: 'Admin Dashboard',
        students: 'Students',
        sessions: 'Sessions',
        weeks: 'Weeks',
        manageStudents: 'Manage Students',
        manageSessions: 'Manage Sessions',
        manageWeeks: 'Manage Weeks',
        importCSV: 'Import CSV',
        createWeek: 'Create Week',
        createSession: 'Create Session',
        addStudent: 'Add Student',
        edit: 'Edit',
        delete: 'Delete',
        save: 'Save',
        cancel: 'Cancel',
        
        // csv
        uploadCSV: 'Upload CSV File',
        csvPreview: 'CSV Preview',
        importStudents: 'Import Students',
        totalRows: 'Total Rows',
        imported: 'Imported',
        skipped: 'Skipped',
        errors: 'Errors',
        
        // week creation
        weekNumber: 'Week Number',
        participantCount: 'Number of Participants',
        randomSelection: 'Random Selection',
        manualSelection: 'Manual Selection',
        gradeFilter: 'Grade Filter',
        resetIfInsufficient: 'Reset session if insufficient students',
        createPartialWeek: 'Create partial week',
        
        // messages
        loading: 'Loading...',
        noData: 'No data available',
        success: 'Success',
        error: 'Error',
        warning: 'Warning',
        confirmDelete: 'Are you sure you want to delete this?',
        deleteSuccess: 'Deleted successfully',
        saveSuccess: 'Saved successfully',
        updateSuccess: 'Updated successfully',
        
        // validation
        required: 'This field is required',
        invalidEmail: 'Invalid email address',
        passwordMismatch: 'Passwords do not match',
        passwordTooShort: 'Password must be at least 6 characters',
        
        // student fields
        fullName: 'Full Name',
        grade: 'Grade',
        active: 'Active',
        inactive: 'Inactive',
        
        // session fields
        sessionNumber: 'Session Number',
        sessionName: 'Session Name',
        startDate: 'Start Date',
        endDate: 'End Date',
        
        // misc
        search: 'Search',
        filter: 'Filter',
        all: 'All',
        actions: 'Actions',
        details: 'Details',
        back: 'Back',
        next: 'Next',
        previous: 'Previous',
        close: 'Close',
        partialWeek: 'Partial Week',
        resetSpeakers: 'Reset Speakers'
    },
    
    ne: {
        // auth
        login: 'लगइन',
        signup: 'साइन अप',
        logout: 'लगआउट',
        email: 'इमेल',
        password: 'पासवर्ड',
        confirmPassword: 'पासवर्ड पुष्टि गर्नुहोस्',
        loginButton: 'लगइन गर्नुहोस्',
        signupButton: 'साइन अप गर्नुहोस्',
        alreadyHaveAccount: 'पहिले नै खाता छ?',
        dontHaveAccount: 'खाता छैन?',
        
        // nav
        dashboard: 'ड्यासबोर्ड',
        winners: 'विजेताहरू',
        adminPanel: 'प्रशासक प्यानल',
        events: 'कार्यक्रमहरू',
        
        // events
        debate: 'बहस',
        presentation: 'प्रस्तुतीकरण',
        extempore: 'तत्काल भाषण',
        selectEvent: 'कार्यक्रम चयन गर्नुहोस्',
        selectLanguage: 'भाषा चयन गर्नुहोस्',
        selectGrade: 'कक्षा चयन गर्नुहोस्',
        
        // language
        english: 'अंग्रेजी',
        nepali: 'नेपाली',
        
        // grades
        grade11: 'कक्षा ११',
        grade12: 'कक्षा १२',
        
        // week details
        week: 'हप्ता',
        session: 'सत्र',
        participants: 'सहभागीहरू',
        judges: 'निर्णायकहरू',
        criteria: 'मूल्याङ्कन मापदण्ड',
        score: 'अंक',
        winner: 'विजेता',
        topic: 'विषय',
        date: 'मिति',
        
        // winners
        recentWinners: 'हालका विजेताहरू',
        position: 'स्थान',
        studentName: 'विद्यार्थीको नाम',
        eventName: 'कार्यक्रम',
        weekNumber: 'हप्ता',
        
        // admin
        adminDashboard: 'प्रशासक ड्यासबोर्ड',
        students: 'विद्यार्थीहरू',
        sessions: 'सत्रहरू',
        weeks: 'हप्ताहरू',
        manageStudents: 'विद्यार्थी व्यवस्थापन',
        manageSessions: 'सत्र व्यवस्थापन',
        manageWeeks: 'हप्ता व्यवस्थापन',
        importCSV: 'CSV आयात गर्नुहोस्',
        createWeek: 'हप्ता सिर्जना गर्नुहोस्',
        createSession: 'सत्र सिर्जना गर्नुहोस्',
        addStudent: 'विद्यार्थी थप्नुहोस्',
        edit: 'सम्पादन गर्नुहोस्',
        delete: 'मेटाउनुहोस्',
        save: 'सुरक्षित गर्नुहोस्',
        cancel: 'रद्द गर्नुहोस्',
        
        // csv
        uploadCSV: 'CSV फाइल अपलोड गर्नुहोस्',
        csvPreview: 'CSV पूर्वावलोकन',
        importStudents: 'विद्यार्थी आयात गर्नुहोस्',
        totalRows: 'कुल पङ्क्तिहरू',
        imported: 'आयात गरियो',
        skipped: 'छोडियो',
        errors: 'त्रुटिहरू',
        
        // week creation
        weekNumber: 'हप्ता नम्बर',
        participantCount: 'सहभागीहरूको संख्या',
        randomSelection: 'अनियमित छनौट',
        manualSelection: 'म्यानुअल छनौट',
        gradeFilter: 'कक्षा फिल्टर',
        resetIfInsufficient: 'अपर्याप्त विद्यार्थी भएमा सत्र रिसेट गर्नुहोस्',
        createPartialWeek: 'आंशिक हप्ता सिर्जना गर्नुहोस्',
        
        // messages
        loading: 'लोड हुँदैछ...',
        noData: 'कुनै डाटा उपलब्ध छैन',
        success: 'सफल',
        error: 'त्रुटि',
        warning: 'चेतावनी',
        confirmDelete: 'के तपाईं यो मेटाउन निश्चित हुनुहुन्छ?',
        deleteSuccess: 'सफलतापूर्वक मेटाइयो',
        saveSuccess: 'सफलतापूर्वक सुरक्षित गरियो',
        updateSuccess: 'सफलतापूर्वक अद्यावधिक गरियो',
        
        // validation
        required: 'यो फिल्ड आवश्यक छ',
        invalidEmail: 'अमान्य इमेल ठेगाना',
        passwordMismatch: 'पासवर्डहरू मेल खाँदैनन्',
        passwordTooShort: 'पासवर्ड कम्तिमा ६ अक्षर हुनुपर्छ',
        
        // student fields
        fullName: 'पूरा नाम',
        grade: 'कक्षा',
        active: 'सक्रिय',
        inactive: 'निष्क्रिय',
        
        // session fields
        sessionNumber: 'सत्र नम्बर',
        sessionName: 'सत्र नाम',
        startDate: 'सुरु मिति',
        endDate: 'अन्त्य मिति',
        
        // misc
        search: 'खोज्नुहोस्',
        filter: 'फिल्टर',
        all: 'सबै',
        actions: 'कार्यहरू',
        details: 'विवरण',
        back: 'पछाडि',
        next: 'अर्को',
        previous: 'अघिल्लो',
        close: 'बन्द गर्नुहोस्',
        partialWeek: 'आंशिक हप्ता',
        resetSpeakers: 'वक्ताहरू रिसेट गर्नुहोस्'
    }
};

class I18n {
    constructor() {
        this.currentLanguage = this.loadLanguage();
    }
    
    loadLanguage() {
        // load saved language
        const saved = localStorage.getItem('language');
        if (saved && (saved === 'en' || saved === 'ne')) {
            return saved;
        }
        return 'en';
    }
    
    setLanguage(lang) {
        if (lang === 'en' || lang === 'ne') {
            this.currentLanguage = lang;
            localStorage.setItem('language', lang);
            this.updatePageTexts();
        }
    }
    
    getLanguage() {
        return this.currentLanguage;
    }
    
    t(key) {
        const keys = key.split('.');
        let value = translations[this.currentLanguage];
        
        for (const k of keys) {
            if (value && typeof value === 'object') {
                value = value[k];
            } else {
                return key;
            }
        }
        
        return value || key;
    }
    
    updatePageTexts() {
        // update text content
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' && element.type !== 'submit') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });
        
        // update placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.t(key);
        });
        
        // sync language dropdown
        const langSelect = document.getElementById('languageSelect');
        if (langSelect) {
            langSelect.value = this.currentLanguage;
        }
    }
}

// global instance
const i18n = new I18n();

// export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = i18n;
}
