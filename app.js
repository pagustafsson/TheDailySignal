/**
 * The Daily Signal - App Logic
 * Handles date display and future daily refresh functionality
 */

(function () {
    'use strict';

    // Format date elegantly (e.g., "Saturday, December 7, 2025")
    function formatDate(date) {
        const options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };
        return date.toLocaleDateString('en-US', options);
    }

    // Update the masthead date
    function updateDate() {
        const dateElement = document.getElementById('current-date');
        if (dateElement) {
            dateElement.textContent = formatDate(new Date());
        }
    }

    // Handle image loading errors gracefully
    function setupImageFallback() {
        const heroImage = document.getElementById('hero-image');
        if (heroImage) {
            heroImage.onerror = function () {
                // Create a placeholder gradient if image fails to load
                this.style.background = 'linear-gradient(135deg, #2c3e50 0%, #4a6741 50%, #1a1a1a 100%)';
                this.style.minHeight = '350px';
                this.alt = 'Image unavailable';
            };
        }
    }

    // Initialize on DOM load
    document.addEventListener('DOMContentLoaded', function () {
        updateDate();
        setupImageFallback();
    });

    // Expose refresh configuration for future automation
    window.DailySignal = {
        refreshTime: '07:00', // CET
        topics: ['AI', 'Quantum Computing', 'Technology Policy'],
        version: '1.0.0'
    };

})();
