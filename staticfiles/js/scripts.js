document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss toasts
    const toastWrapper = document.getElementById('toastWrapper');
    if (toastWrapper) {
        setTimeout(() => {
            toastWrapper.style.transition = 'opacity 0.5s ease';
            toastWrapper.style.opacity = '0';
            setTimeout(() => toastWrapper.remove(), 500);
        }, 5000);
    }

    // Navbar scroll effect
    const topbar = document.querySelector('.dash-topbar, .admin-topbar, .landing-topbar');
    if (topbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 30) {
                topbar.style.background = 'rgba(6, 6, 11, 0.95)';
                topbar.style.borderBottomColor = 'rgba(255,255,255,0.05)';
            } else {
                topbar.style.background = '';
                topbar.style.borderBottomColor = '';
            }
        });
    }

    // Color preview
    const colorSelect = document.querySelector('select[name="color"]');
    const preview = document.getElementById('colorPreview');
    if (colorSelect && preview) {
        function updatePreview() {
            preview.style.backgroundColor = colorSelect.value;
        }
        colorSelect.addEventListener('change', updatePreview);
        updatePreview();
    }

    console.log('⚡ HabitFlow v3 loaded');
});