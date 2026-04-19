document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss toasts
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        const bsToast = new bootstrap.Toast(toast, { delay: 5000 });
        bsToast.show();
    });

    // Smooth navbar on scroll
    const navbar = document.querySelector('.dashboard-nav, .admin-nav, .landing-nav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(10, 10, 26, 0.95)';
                navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
            } else {
                navbar.style.background = '';
                navbar.style.boxShadow = '';
            }
        });
    }

    // Ripple effect on buttons
    document.querySelectorAll('.btn-hover-glow').forEach(btn => {
        btn.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
            ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.2)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'rippleEffect 0.6s ease-out';
            ripple.style.pointerEvents = 'none';
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Ripple keyframes
    if (!document.getElementById('ripple-style')) {
        const style = document.createElement('style');
        style.id = 'ripple-style';
        style.textContent = '@keyframes rippleEffect { to { transform: scale(4); opacity: 0; } }';
        document.head.appendChild(style);
    }

    // Habit card tilt effect
    document.querySelectorAll('.habit-card').forEach(card => {
        card.addEventListener('mousemove', function (e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const rotateX = (y - rect.height / 2) / 30;
            const rotateY = (rect.width / 2 - x) / 30;
            this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
        });
        card.addEventListener('mouseleave', function () {
            this.style.transform = '';
        });
    });

    // Color preview for habit form
    const colorSelect = document.querySelector('select[name="color"]');
    if (colorSelect) {
        const updateColor = () => {
            colorSelect.style.borderLeftWidth = '4px';
            colorSelect.style.borderLeftColor = colorSelect.value;
        };
        colorSelect.addEventListener('change', updateColor);
        updateColor();
    }

    console.log('⚡ HabitFlow loaded');
});