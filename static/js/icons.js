function createUiIcon(svg, className = '') {
    const classes = ['ui-icon'];

    if (className) {
        classes.push(className);
    }

    return `<span class="${classes.join(' ')}" aria-hidden="true">${svg}</span>`;
}

function iconSvg(paths) {
    return `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" focusable="false">
            ${paths}
        </svg>
    `;
}

window.AppIcons = {
    trophy(className = '') {
        return createUiIcon(iconSvg(`
            <path d="M8 4h8v3a4 4 0 0 1-8 0V4Z"></path>
            <path d="M7 6H5a2 2 0 0 0 2 2"></path>
            <path d="M17 6h2a2 2 0 0 1-2 2"></path>
            <path d="M10 11v2.5a2 2 0 0 1-1 1.73l-1.5.87"></path>
            <path d="M14 11v2.5a2 2 0 0 0 1 1.73l1.5.87"></path>
            <path d="M9 20h6"></path>
            <path d="M10.5 14h3V20h-3z"></path>
        `), `icon-trophy ${className}`.trim());
    },

    publish(className = '') {
        return createUiIcon(iconSvg(`
            <path d="M5 12h7"></path>
            <path d="M11 8l8 4-8 4V8Z"></path>
            <path d="M13 12h6"></path>
        `), `icon-publish ${className}`.trim());
    },

    unpublish(className = '') {
        return createUiIcon(iconSvg(`
            <circle cx="12" cy="12" r="8"></circle>
            <path d="M8.5 8.5l7 7"></path>
        `), `icon-unpublish ${className}`.trim());
    },

    crown(className = '') {
        return createUiIcon(iconSvg(`
            <path d="M4 16h16l-1.5-9-4.5 4-2-5-2 5-4.5-4L4 16Z"></path>
            <path d="M6 19h12"></path>
        `), `icon-crown ${className}`.trim());
    },

    medal(tone = 'gold', className = '') {
        return createUiIcon(iconSvg(`
            <path d="M8 3h3.5L12 6l.5-3H16l-2.5 5.5"></path>
            <path d="M16 3h-3.5L12 6l-.5-3H8l2.5 5.5"></path>
            <circle cx="12" cy="14" r="5.5"></circle>
            <path d="M12 11.5l1 2 2.2.3-1.6 1.5.4 2.1-2-1-2 1 .4-2.1-1.6-1.5 2.2-.3 1-2Z"></path>
        `), `icon-medal icon-medal--${tone} ${className}`.trim());
    }
};