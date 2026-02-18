// auth class

class Auth {
    constructor() {
        this.token = localStorage.getItem('access_token');
        this.user = JSON.parse(localStorage.getItem('user') || 'null');
        this.isAdmin = false; // always verify from server
        localStorage.removeItem('is_admin'); // clear any stale value
    }
    
    async signup(email, password) {
        try {
            const response = await fetch('/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Signup failed');
            }
            
            // save session if one was returned
            if (data.session && data.session.access_token) {
                this.setSession(data.session.access_token, data.user, false);
            }
            
            return data;
        } catch (error) {
            throw error;
        }
    }
    
    async login(email, password) {
        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Login failed');
            }
            
            // save session
            this.setSession(data.session.access_token, data.user, data.is_admin);
            
            return data;
        } catch (error) {
            throw error;
        }
    }
    
    async logout() {
        try {
            if (this.token) {
                await fetch('/auth/logout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    }
                });
            }
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            this.clearSession();
        }
    }
    
    async verifyToken() {
        if (!this.token) {
            return false;
        }
        
        try {
            const response = await fetch('/auth/verify', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
            
            if (!response.ok) {
                this.clearSession();
                return false;
            }
            
            const data = await response.json();
            this.user = data.user;
            this.isAdmin = data.is_admin; // from server only, never stored locally
            localStorage.setItem('user', JSON.stringify(data.user));
            
            return true;
        } catch (error) {
            this.clearSession();
            return false;
        }
    }
    
    setSession(token, user, isAdmin) {
        this.token = token;
        this.user = user;
        this.isAdmin = isAdmin;
        
        localStorage.setItem('access_token', token);
        localStorage.setItem('user', JSON.stringify(user));
        // is_admin stays in memory only
    }
    
    clearSession() {
        this.token = null;
        this.user = null;
        this.isAdmin = false;
        
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        localStorage.removeItem('selected_event');
        localStorage.removeItem('selected_grade');
    }
    
    isAuthenticated() {
        return !!this.token;
    }
    
    getToken() {
        return this.token;
    }
    
    getUser() {
        return this.user;
    }
    
    checkAdmin() {
        return this.isAdmin;
    }
    
    getAuthHeaders() {
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`
        };
    }
}

// global auth instance
const auth = new Auth();

// redirects to login if not authenticated
async function requireAuth() {
    if (!auth.isAuthenticated()) {
        window.location.href = '/';
        return false;
    }
    
    const valid = await auth.verifyToken();
    if (!valid) {
        window.location.href = '/';
        return false;
    }
    
    return true;
}

// redirects away if not an admin
async function requireAdmin() {
    const authenticated = await requireAuth();
    if (!authenticated) {
        return false;
    }
    
    if (!auth.checkAdmin()) {
        alert(i18n.t('error') + ': Admin access required');
        // redirect to the correct language side's dashboard
        const lang = window.APP_LANG || localStorage.getItem('language') || 'en';
        window.location.href = '/' + lang + '/dashboard';
        return false;
    }
    
    return true;
}

// show/hide elements based on auth state
function updateUIForAuth() {
    const isAuth = auth.isAuthenticated();
    const isAdmin = auth.checkAdmin();
    
    // hide admin-only elements for non-admins
    document.querySelectorAll('[data-admin-only]').forEach(el => {
        el.style.display = isAdmin ? '' : 'none';
    });
    
    // hide auth-required elements when logged out
    document.querySelectorAll('[data-auth-required]').forEach(el => {
        el.style.display = isAuth ? '' : 'none';
    });
}

// export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { auth, requireAuth, requireAdmin, updateUIForAuth };
}
