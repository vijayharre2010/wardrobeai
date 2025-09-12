// Persistent premium upgrade popup for non-premium users
class PremiumPopup {
    constructor() {
        this.popup = null;
        this.isVisible = false;
        this.dismissedUntil = 0;
        this.checkInterval = null;
        this.init();
    }

    async init() {
        // Check if user is logged in and not premium
        try {
            const response = await fetch('/check_subscription');
            const data = await response.json();

            if (!data.is_premium) {
                this.createPopup();
                this.startPopupCycle();
            }
        } catch (error) {
            console.error('Failed to check subscription status:', error);
        }
    }

    createPopup() {
        // Create popup container
        this.popup = document.createElement('div');
        this.popup.id = 'premium-popup';
        this.popup.innerHTML = `
            <div class="popup-content">
                <button class="popup-close" onclick="premiumPopup.hide()">
                    <i data-lucide="x" class="icon-small"></i>
                </button>

                <div class="popup-header">
                    <i data-lucide="crown" class="icon" style="color: #B19CD9;"></i>
                    <h3>Unlock Unlimited Access!</h3>
                </div>

                <div class="popup-body">
                    <p>Get personalized outfit suggestions and AI image generation without limits.</p>
                    <div class="popup-features">
                        <div class="feature-item">
                            <i data-lucide="check" class="icon-small" style="color: #4ecdc4;"></i>
                            <span>Unlimited daily suggestions</span>
                        </div>
                        <div class="feature-item">
                            <i data-lucide="check" class="icon-small" style="color: #4ecdc4;"></i>
                            <span>AI outfit generation</span>
                        </div>
                        <div class="feature-item">
                            <i data-lucide="check" class="icon-small" style="color: #4ecdc4;"></i>
                            <span>Advanced personalization</span>
                        </div>
                    </div>
                </div>

                <div class="popup-footer">
                    <div class="pricing">
                        <span class="original-price">$29.97</span>
                        <span class="discounted-price">$26.97/month</span>
                        <span class="savings">Save $3!</span>
                    </div>
                    <a href="/page/profile#premium" class="popup-upgrade-btn">
                        Upgrade Now
                    </a>
                </div>
            </div>
        `;

        document.body.appendChild(this.popup);

        // Initialize Lucide icons for the popup
        if (window.lucide && typeof window.lucide.createIcons === 'function') {
            window.lucide.createIcons();
        }
    }

    show() {
        if (!this.popup || this.isVisible) return;

        this.popup.style.display = 'flex';
        this.isVisible = true;

        // Add fade-in animation
        setTimeout(() => {
            this.popup.classList.add('visible');
        }, 10);
    }

    hide() {
        if (!this.popup || !this.isVisible) return;

        this.popup.classList.remove('visible');
        this.isVisible = false;

        // Set dismissal timer (5 minutes)
        this.dismissedUntil = Date.now() + (5 * 60 * 1000);

        setTimeout(() => {
            this.popup.style.display = 'none';
        }, 300);
    }

    startPopupCycle() {
        // Show popup after 30 seconds
        setTimeout(() => {
            if (!this.isVisible && Date.now() > this.dismissedUntil) {
                this.show();
            }
        }, 30000);

        // Check every 2 minutes if popup should be shown
        this.checkInterval = setInterval(() => {
            if (!this.isVisible && Date.now() > this.dismissedUntil) {
                // Only show on certain pages
                const currentPath = window.location.pathname;
                const allowedPages = ['/page/dashboard', '/page/daily', '/page/generate'];

                if (allowedPages.some(page => currentPath.startsWith(page))) {
                    this.show();
                }
            }
        }, 120000); // 2 minutes
    }

    destroy() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
        }
        if (this.popup) {
            this.popup.remove();
        }
    }
}

// Initialize popup when DOM is ready
let premiumPopup;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        premiumPopup = new PremiumPopup();
    });
} else {
    premiumPopup = new PremiumPopup();
}

// Make popup available globally
window.premiumPopup = premiumPopup;