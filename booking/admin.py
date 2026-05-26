from django.contrib import admin
from .models import Booking

# Optional: nice admin display
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'total_price', 'created_at')
    list_filter = ('check_in', 'room')
    search_fields = ('user__username', 'room__name')

admin.site.register(Booking, BookingAdmin)