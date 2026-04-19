document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss toasts after 5s
    const toastWrapper = document.getElementById('toastWrapper');
    if (toastWrapper) {
        setTimeout(() => {
            toastWrapper.style.transition = 'opacity 0.4s ease';
            toastWrapper.style.opacity = '0';
            setTimeout(() => toastWrapper.remove(), 400);
        }, 5000);
    }

    // Smooth navbar opacity on scroll
    const topbar = document.querySelector('.dash-topbar, .admin-topbar, .landing-topbar');
    if (topbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 30) {
                topbar.style.background = 'rgba(10, 10, 15, 0.95)';
            } else {
                topbar.style.background = '';
            }
        });
    }

    // Color preview on habit forms
    const colorSelect = document.querySelector('select[name="color"]');
    const preview = document.getElementById('colorPreview');
    if (colorSelect && preview) {
        function updatePreview() {
            preview.style.backgroundColor = colorSelect.value;
        }
        colorSelect.addEventListener('change', updatePreview);
        updatePreview();
    }

    console.log('⚡ HabitFlow loaded');
});