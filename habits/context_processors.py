def user_context(request):
    context = {
        'is_admin_user': False,
    }
    if request.user.is_authenticated:
        context['is_admin_user'] = request.user.is_staff or request.user.is_superuser
    return context