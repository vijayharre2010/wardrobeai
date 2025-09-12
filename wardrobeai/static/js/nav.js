// Dynamically load bottom navigation tabs with enhanced styling
async function loadNavigation() {
    try {
        const res = await fetch('/api/pages');
        const data = await res.json();
        const pages = data.pages || [];
        const nav = document.getElementById('nav-tabs');

        if (!nav) {
            console.error('Navigation element not found');
            return;
        }

        // Clear existing navigation
        nav.innerHTML = '';

        const iconMap = {
            'dashboard': 'layout-dashboard',
            'daily': 'sun',
            'generate': 'image',
            'profile': 'user'
        };

        const labelMap = {
            'dashboard': 'Dashboard',
            'daily': 'Daily',
            'generate': 'Generate',
            'profile': 'Profile'
        };

        pages.forEach(page => {
            const li = document.createElement('li');
            const link = document.createElement('a');
            link.href = `/page/${page}`;
            link.title = labelMap[page] || page.charAt(0).toUpperCase() + page.slice(1);

            // Add icon
            const iconName = iconMap[page] || 'circle';
            const icon = document.createElement('i');
            icon.setAttribute('data-lucide', iconName);
            icon.className = 'icon';
            link.appendChild(icon);

            // Add text
            const text = document.createElement('span');
            text.innerText = labelMap[page] || page.charAt(0).toUpperCase() + page.slice(1);
            text.style.fontSize = '0.7rem';
            text.style.fontWeight = '600';
            text.style.textTransform = 'uppercase';
            text.style.letterSpacing = '0.5px';
            link.appendChild(text);

            li.appendChild(link);
            nav.appendChild(li);
        });

        // Add smooth scrolling and active state management
        const navLinks = nav.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Remove active class from all links
                navLinks.forEach(l => l.classList.remove('active'));
                // Add active class to clicked link
                this.classList.add('active');
            });
        });

        // Set active state based on current URL
        const currentPath = window.location.pathname;
        navLinks.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });

        // Re-initialize Lucide icons after adding new elements
        if (window.lucide && typeof window.lucide.createIcons === 'function') {
            window.lucide.createIcons();
        }

    } catch (error) {
        console.error('Failed to load navigation:', error);
    }
}

// Load navigation when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadNavigation);
} else {
    loadNavigation();
}
