// Main frontend logic
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth entrance animation to main content
    const content = document.querySelector('.content');
    if (content) {
        content.style.opacity = '0';
        content.style.transform = 'translateY(20px)';
        content.style.transition = 'opacity 0.6s ease, transform 0.6s ease';

        setTimeout(() => {
            content.style.opacity = '1';
            content.style.transform = 'translateY(0)';
        }, 100);
    }

    // Add stagger effect to stat cards if they exist
    const cards = document.querySelectorAll('.stat-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        card.style.transitionDelay = `${index * 0.15 + 0.3}s`;

        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100);
    });

    // Slot card animations in parking grid
    const slots = document.querySelectorAll('.slot-card');
    slots.forEach((slot, index) => {
        slot.style.opacity = '0';
        slot.style.transform = 'scale(0.9)';
        slot.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        // Stagger load based on index
        slot.style.transitionDelay = `${index * 0.05}s`;

        setTimeout(() => {
            slot.style.opacity = '1';
            slot.style.transform = 'scale(1)';
        }, 100);
    });

    // Auto-hide success alerts after 5 seconds
    const successAlert = document.querySelector('.alert-success');
    if (successAlert) {
        setTimeout(() => {
            successAlert.style.transition = 'opacity 0.5s ease';
            successAlert.style.opacity = '0';
            setTimeout(() => {
                successAlert.style.display = 'none';
            }, 500);
        }, 5000);
    }

    // Theme Toggler Logic
    const themeBtn = document.getElementById('theme-toggle');
    const iconSun = document.getElementById('theme-icon-sun');
    const iconMoon = document.getElementById('theme-icon-moon');
    
    // Check saved theme
    if (localStorage.getItem('theme') === 'light' || (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: light)').matches)) {
        document.documentElement.classList.add('light-mode');
        if (iconMoon && iconSun) {
            iconMoon.style.display = 'none';
            iconSun.style.display = 'block';
        }
    } else {
        document.documentElement.classList.remove('light-mode');
    }

    if (themeBtn) {
        themeBtn.addEventListener('click', async (e) => {
            const isDark = !document.documentElement.classList.contains('light-mode');
            
            const toggleTheme = () => {
                if (isDark) {
                    document.documentElement.classList.add('light-mode');
                    localStorage.setItem('theme', 'light');
                    iconMoon.style.display = 'none';
                    iconSun.style.display = 'block';
                } else {
                    document.documentElement.classList.remove('light-mode');
                    localStorage.setItem('theme', 'dark');
                    iconSun.style.display = 'none';
                    iconMoon.style.display = 'block';
                }
            };

            if (!document.startViewTransition) {
                toggleTheme();
                return;
            }

            const rect = themeBtn.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            const maxDistance = Math.hypot(
                Math.max(centerX, innerWidth - centerX),
                Math.max(centerY, innerHeight - centerY)
            );

            if (!isDark) {
                document.documentElement.classList.add('theme-transition-reversing');
            }

            const transition = document.startViewTransition(toggleTheme);
            
            transition.ready.then(() => {
                const clipPath = [
                    `circle(0px at ${centerX}px ${centerY}px)`,
                    `circle(${maxDistance}px at ${centerX}px ${centerY}px)`
                ];
                
                document.documentElement.animate(
                    {
                        clipPath: isDark ? clipPath : clipPath.slice().reverse()
                    },
                    {
                        duration: 700,
                        easing: "ease-in-out",
                        pseudoElement: isDark ? "::view-transition-new(root)" : "::view-transition-old(root)",
                        fill: "forwards"
                    }
                );
            });

            transition.finished.then(() => {
                document.documentElement.classList.remove('theme-transition-reversing');
            });
        });
    }
});
