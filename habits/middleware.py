from django.shortcuts import redirect


class AdminRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            if request.user.profile.is_deactivated:
                allowed_paths = ['/logout/', '/login/', '/']
                if request.path not in allowed_paths:
                    from django.contrib.auth import logout
                    from django.contrib import messages
                    logout(request)
                    messages.error(request, 'Your account has been deactivated.')
                    return redirect('login')

        response = self.get_response(request)
        return response