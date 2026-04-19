from django.contrib import admin
from .models import Habit, HabitLog, UserProfile


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'frequency', 'is_active', 'created_at')
    list_filter = ('category', 'frequency', 'is_active')
    search_fields = ('name', 'user__username')


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('habit', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'completed_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_deactivated', 'created_at')
    list_filter = ('is_deactivated',)