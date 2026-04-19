from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta
from .models import Habit, HabitLog, UserProfile
from .forms import CustomUserCreationForm, CustomAuthenticationForm, HabitForm


def is_admin(user):
    return user.is_staff or user.is_superuser


def ensure_profile(user):
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ensure_profile(user)
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Start by adding your first habit.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            profile = ensure_profile(user)
            if profile.is_deactivated:
                messages.error(request, 'Your account has been deactivated. Contact support.')
                return redirect('login')
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('landing')


@login_required
def dashboard(request):
    profile = ensure_profile(request.user)
    habits = request.user.habits.filter(is_active=True)
    today = timezone.now().date()

    total_habits = habits.count()
    completed_today = sum(1 for h in habits if h.is_completed_today())
    skipped_today = sum(1 for h in habits if h.is_skipped_today())
    overall_progress = profile.get_overall_progress()
    best_streak = max((h.get_streak() for h in habits), default=0)

    habit_data = []
    for habit in habits:
        today_log = habit.logs.filter(completed_at__date=today).first()
        status = 'pending'
        if today_log:
            if today_log.is_completed:
                status = 'completed'
            elif today_log.is_skipped:
                status = 'skipped'

        habit_data.append({
            'habit': habit,
            'progress': habit.get_progress_percentage(),
            'completed': status == 'completed',
            'skipped': status == 'skipped',
            'status': status,
            'streak': habit.get_streak(),
            'weekly': habit.get_weekly_data(),
            'today_count': habit.today_completion_count(),
            'today_log': today_log,
        })

    context = {
        'habits': habit_data,
        'total_habits': total_habits,
        'completed_today': completed_today,
        'skipped_today': skipped_today,
        'overall_progress': overall_progress,
        'best_streak': best_streak,
        'today': today,
        'profile': profile,
    }
    return render(request, 'dashboard.html', context)


@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            try:
                habit.save()
                messages.success(request, f'"{habit.name}" has been added!')
            except Exception:
                messages.error(request, 'A habit with that name already exists.')
            return redirect('dashboard')
    else:
        form = HabitForm()
    return render(request, 'habit_form.html', {'form': form, 'title': 'Add New Habit'})


@login_required
def habit_edit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{habit.name}" has been updated!')
            return redirect('dashboard')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habit_edit.html', {'form': form, 'habit': habit, 'title': 'Edit Habit'})


@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        name = habit.name
        habit.delete()
        messages.success(request, f'"{name}" has been deleted.')
        return redirect('dashboard')
    return render(request, 'habit_delete.html', {'habit': habit})


@login_required
def habit_mark(request, pk, action):
    """Mark a habit as completed or skipped for today. Allows re-editing."""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()

    if request.method == 'POST':
        today_log = habit.logs.filter(completed_at__date=today).first()

        if action == 'complete':
            if today_log:
                today_log.is_completed = True
                today_log.is_skipped = False
                today_log.completed_at = timezone.now()
                today_log.save()
            else:
                HabitLog.objects.create(
                    habit=habit,
                    is_completed=True,
                    is_skipped=False,
                    completed_at=timezone.now()
                )
            message = f'"{habit.name}" marked as completed!'
            status = 'completed'

        elif action == 'skip':
            if today_log:
                today_log.is_completed = False
                today_log.is_skipped = True
                today_log.completed_at = timezone.now()
                today_log.save()
            else:
                HabitLog.objects.create(
                    habit=habit,
                    is_completed=False,
                    is_skipped=True,
                    completed_at=timezone.now()
                )
            message = f'"{habit.name}" marked as skipped.'
            status = 'skipped'

        elif action == 'undo':
            if today_log:
                today_log.delete()
            message = f'"{habit.name}" reset to pending.'
            status = 'pending'

        else:
            messages.error(request, 'Invalid action.')
            return redirect('dashboard')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': status,
                'progress': habit.get_progress_percentage(),
                'streak': habit.get_streak(),
                'today_count': habit.today_completion_count(),
                'target_count': habit.target_count,
                'message': message,
            })

        messages.success(request, message)
    return redirect('dashboard')


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all().select_related('profile').prefetch_related('habits')
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    total_users = users.exclude(is_superuser=True).count()
    active_today = User.objects.filter(
        habits__logs__completed_at__date=today
    ).distinct().count()
    total_habits = Habit.objects.filter(user__is_superuser=False).count()
    total_logs_week = HabitLog.objects.filter(
        completed_at__date__gte=week_ago, is_completed=True
    ).count()

    user_data = []
    for user in users.exclude(is_superuser=True).order_by('-date_joined'):
        profile = ensure_profile(user)
        user_habits = user.habits.filter(is_active=True)
        completions_today = sum(1 for h in user_habits if h.is_completed_today())
        total_user_habits = user_habits.count()

        user_data.append({
            'user': user,
            'profile': profile,
            'total_habits': total_user_habits,
            'completed_today': completions_today,
            'progress': profile.get_overall_progress(),
            'last_active': HabitLog.objects.filter(
                habit__user=user
            ).order_by('-completed_at').first(),
            'is_deactivated': profile.is_deactivated,
        })

    search = request.GET.get('search', '')
    if search:
        user_data = [u for u in user_data if
                     search.lower() in u['user'].username.lower() or
                     search.lower() in u['user'].email.lower() or
                     search.lower() in (u['user'].first_name or '').lower()]

    filter_by = request.GET.get('filter', 'all')
    if filter_by == 'active':
        user_data = [u for u in user_data if not u['is_deactivated']]
    elif filter_by == 'deactivated':
        user_data = [u for u in user_data if u['is_deactivated']]

    context = {
        'user_data': user_data,
        'total_users': total_users,
        'active_today': active_today,
        'total_habits': total_habits,
        'total_logs_week': total_logs_week,
        'search': search,
        'filter_by': filter_by,
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_user_detail(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    profile = ensure_profile(target_user)
    habits = target_user.habits.filter(is_active=True)
    recent_logs = HabitLog.objects.filter(
        habit__user=target_user
    ).select_related('habit').order_by('-completed_at')[:50]

    habit_data = []
    for habit in habits:
        habit_data.append({
            'habit': habit,
            'progress': habit.get_progress_percentage(),
            'streak': habit.get_streak(),
            'total_completions': habit.logs.filter(is_completed=True).count(),
            'weekly': habit.get_weekly_data(),
        })

    context = {
        'target_user': target_user,
        'profile': profile,
        'habit_data': habit_data,
        'recent_logs': recent_logs,
    }
    return render(request, 'admin_user_detail.html', context)


@login_required
@user_passes_test(is_admin)
def admin_toggle_user(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    if target_user == request.user:
        messages.error(request, "You can't deactivate your own account!")
        return redirect('admin_dashboard')

    profile = ensure_profile(target_user)
    if profile.is_deactivated:
        profile.is_deactivated = False
        profile.deactivated_at = None
        profile.save()
        target_user.is_active = True
        target_user.save()
        messages.success(request, f'{target_user.username} has been reactivated.')
    else:
        profile.is_deactivated = True
        profile.deactivated_at = timezone.now()
        profile.save()
        target_user.is_active = False
        target_user.save()
        messages.warning(request, f'{target_user.username} has been deactivated.')

    return redirect('admin_dashboard')


@login_required
@user_passes_test(is_admin)
def admin_delete_user(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    if target_user == request.user:
        messages.error(request, "You can't delete your own account!")
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = target_user.username
        target_user.delete()
        messages.success(request, f'User "{username}" has been permanently deleted.')
        return redirect('admin_dashboard')

    return redirect('admin_dashboard')