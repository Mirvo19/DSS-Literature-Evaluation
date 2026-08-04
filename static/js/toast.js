/**
 * DSS Talk - Modern Toast Notification System
 */

class ToastSystem {
    constructor() {
        this.container = null;
        this.queueKey = 'dss_pending_toasts';
        this._init();
    }

    _init() {
        if (typeof window === 'undefined') return;

        // Ensure container exists on DOM load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.flushQueue());
        } else {
            this.flushQueue();
        }
    }

    _getOrCreateContainer() {
        if (this.container && document.body.contains(this.container)) {
            return this.container;
        }
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        this.container = container;
        return container;
    }

    _getIcon(type) {
        switch (type) {
            case 'success':
                return `<svg class="toast-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>`;
            case 'error':
                return `<svg class="toast-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>`;
            case 'warning':
                return `<svg class="toast-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`;
            case 'info':
            default:
                return `<svg class="toast-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`;
        }
    }

    show({ type = 'info', title = '', message = '', duration = 4500 }) {
        if (typeof window === 'undefined') return;

        const container = this._getOrCreateContainer();

        if (typeof title === 'object') {
            const options = title;
            type = options.type || type;
            message = options.message || message;
            title = options.title || '';
            duration = options.duration || duration;
        } else if (!message && title) {
            message = title;
            title = '';
        }

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const titleHtml = title ? `<div class="toast-title">${title}</div>` : '';
        const iconSvg = this._getIcon(type);

        toast.innerHTML = `
            <div class="toast-header-icon">${iconSvg}</div>
            <div class="toast-body">
                ${titleHtml}
                <div class="toast-message">${message}</div>
            </div>
            <button type="button" class="toast-close" aria-label="Close">&times;</button>
            <div class="toast-progress"><div class="toast-progress-bar"></div></div>
        `;

        container.appendChild(toast);

        // Force reflow for enter animation
        void toast.offsetWidth;
        toast.classList.add('toast-show');

        const progressBar = toast.querySelector('.toast-progress-bar');
        if (progressBar) {
            progressBar.style.transition = `width ${duration}ms linear`;
            requestAnimationFrame(() => {
                progressBar.style.width = '0%';
            });
        }

        let timer = null;
        let startTime = Date.now();
        let remaining = duration;

        const startTimer = () => {
            startTime = Date.now();
            timer = setTimeout(() => {
                this.dismiss(toast);
            }, remaining);
        };

        startTimer();

        // Pause on hover
        toast.addEventListener('mouseenter', () => {
            clearTimeout(timer);
            remaining -= Date.now() - startTime;
            if (progressBar) {
                const currentWidth = getComputedStyle(progressBar).width;
                progressBar.style.transition = 'none';
                progressBar.style.width = currentWidth;
            }
        });

        toast.addEventListener('mouseleave', () => {
            if (remaining > 0) {
                if (progressBar) {
                    progressBar.style.transition = `width ${remaining}ms linear`;
                    progressBar.style.width = '0%';
                }
                startTimer();
            }
        });

        // Close button click
        toast.querySelector('.toast-close').addEventListener('click', () => {
            clearTimeout(timer);
            this.dismiss(toast);
        });

        return toast;
    }

    dismiss(toast) {
        if (!toast || !toast.parentNode) return;
        toast.classList.remove('toast-show');
        toast.classList.add('toast-hide');
        toast.addEventListener('animationend', () => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, { once: true });
    }

    success(message, title = '', duration = 4500) {
        return this.show({ type: 'success', title, message, duration });
    }

    error(message, title = '', duration = 5000) {
        return this.show({ type: 'error', title, message, duration });
    }

    info(message, title = '', duration = 4500) {
        return this.show({ type: 'info', title, message, duration });
    }

    warning(message, title = '', duration = 5000) {
        return this.show({ type: 'warning', title, message, duration });
    }

    // Queue a toast to show after page redirect
    queue(toastConfig) {
        try {
            const existing = JSON.parse(sessionStorage.getItem(this.queueKey) || '[]');
            existing.push(toastConfig);
            sessionStorage.setItem(this.queueKey, JSON.stringify(existing));
        } catch (e) {
            console.error('Failed to queue toast:', e);
        }
    }

    // Flush and show queued toasts
    flushQueue() {
        try {
            const pending = sessionStorage.getItem(this.queueKey);
            if (pending) {
                sessionStorage.removeItem(this.queueKey);
                const items = JSON.parse(pending);
                if (Array.isArray(items)) {
                    items.forEach((item, index) => {
                        setTimeout(() => {
                            this.show(item);
                        }, index * 250);
                    });
                }
            }
        } catch (e) {
            console.error('Failed to flush toast queue:', e);
        }
    }
}

// Instantiate global Toast object
window.Toast = new ToastSystem();
