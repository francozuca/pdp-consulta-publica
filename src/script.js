// Calculate days remaining until the consultation closes
function calculateDaysRemaining() {
    const closingDate = new Date('2026-01-26');
    const today = new Date();
    
    // Reset time to midnight for accurate day calculation
    today.setHours(0, 0, 0, 0);
    closingDate.setHours(0, 0, 0, 0);
    
    const timeDifference = closingDate - today;
    const daysRemaining = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));
    
    return daysRemaining;
}

// Update the days remaining display
function updateDaysRemaining() {
    const daysRemaining = calculateDaysRemaining();
    const daysElement = document.getElementById('days-remaining');
    
    if (daysElement) {
        if (daysRemaining > 0) {
            daysElement.textContent = daysRemaining;
        } else if (daysRemaining === 0) {
            daysElement.textContent = '0 (último día)';
            daysElement.parentElement.style.color = '#e74c3c';
        } else {
            daysElement.textContent = '0 (cerrada)';
            daysElement.parentElement.style.color = '#e74c3c';
        }
    }
}

// Smooth scroll for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Add animation on scroll
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all sections
    document.querySelectorAll('section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    updateDaysRemaining();
    initSmoothScroll();
    initScrollAnimations();
    
    // Update days remaining every hour
    setInterval(updateDaysRemaining, 3600000); // 1 hour in milliseconds
});

// Add click tracking for external links
document.addEventListener('DOMContentLoaded', function() {
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    externalLinks.forEach(link => {
        link.addEventListener('click', function() {
            // You could add analytics tracking here if needed
            console.log('External link clicked:', this.href);
        });
    });
});
