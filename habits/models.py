from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Habit(models.Model):
    CATEGORY_CHOICES = [
        ('health', 'Health & Fitness'),
        ('mind', 'Mind & Learning'),
        ('productivity', 'Productivity'),
        ('social', 'Social'),
        ('creativity', 'Creativity'),
        ('wellness', 'Wellness'),
        ('finance', 'Finance'),
        ('other', 'Other'),
    ]

    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    COLOR_CHOICES = [
        ('#FF6B6B', 'Coral Red'),
        ('#4ECDC4', 'Teal'),
        ('#45B7D1', 'Sky Blue'),
        ('#96CEB4', 'Sage Green'),
        ('#FFEAA7', 'Sunny Yellow'),
        ('#DDA0DD', 'Plum'),
        ('#98D8C8', 'Mint'),
        ('#F7DC6F', 'Gold'),
        ('#BB8FCE', 'Lavender'),
        ('#F0B27A', 'Peach'),
        ('#82E0AA', 'Emerald'),
        ('#85C1E9', 'Light Blue'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#4ECDC4')
    target_count = models.PositiveIntegerField(default=1, help_text='How many times per period')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    def get_today_logs(self):
        today = timezone.now().date()
        return self.logs.filter(completed_at__date=today)

    def is_completed_today(self):
        today = timezone.now().date()
        return self.logs.filter(completed_at__date=today, is_completed=True).exists()

    def is_skipped_today(self):
        today = timezone.now().date()
        return self.logs.filter(completed_at__date=today, is_skipped=True).exists()

    def today_completion_count(self):
        return self.get_today_logs().filter(is_completed=True).count()

    def get_progress_percentage(self):
        if self.is_completed_today():
            return 100
        if self.is_skipped_today():
            return 0
        return 0

    def get_streak(self):
        streak = 0
        current_date = timezone.now().date()
        for i in range(365):
            check_date = current_date - timedelta(days=i)
            day_logs = self.logs.filter(
                completed_at__date=check_date,
                is_completed=True
            )
            if day_logs.exists():
                streak += 1
            elif i == 0:
                continue
            else:
                break
        return streak

    def get_weekly_data(self):
        today = timezone.now().date()
        weekly = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            log = self.logs.filter(completed_at__date=day).first()
            status = 'pending'
            if log:
                if log.is_completed:
                    status = 'completed'
                elif log.is_skipped:
                    status = 'skipped'
            weekly.append({
                'date': day,
                'day_name': day.strftime('%a'),
                'status': status,
                'completed': status == 'completed',
            })
        return weekly


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    is_completed = models.BooleanField(default=False)
    is_skipped = models.BooleanField(default=False)
    completed_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        if self.is_completed:
            status = "Completed"
        elif self.is_skipped:
            status = "Skipped"
        else:
            status = "Pending"
        return f"{status} - {self.habit.name} - {self.completed_at.strftime('%Y-%m-%d')}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_color = models.CharField(max_length=7, default='#4ECDC4')
    timezone = models.CharField(max_length=50, default='UTC')
    is_deactivated = models.BooleanField(default=False)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile: {self.user.username}"

    def get_total_habits(self):
        return self.user.habits.filter(is_active=True).count()

    def get_completed_today(self):
        return sum(1 for h in self.user.habits.filter(is_active=True) if h.is_completed_today())

    def get_overall_progress(self):
        active = self.user.habits.filter(is_active=True)
        if not active.exists():
            return 0
        total_progress = sum(h.get_progress_percentage() for h in active)
        return int(total_progress / active.count())