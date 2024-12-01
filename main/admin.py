from django.contrib import admin

# Register your models here.
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'button_class')
    
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')