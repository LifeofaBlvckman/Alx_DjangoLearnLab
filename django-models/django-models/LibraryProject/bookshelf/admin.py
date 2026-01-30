from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Book, UserProfile

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'user_email')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

# Add UserProfile inline to User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Re-register User admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
