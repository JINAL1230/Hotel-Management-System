from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.models import User
import calendar
from rooms.models import Room
from booking.models import Booking


# ❌ REMOVED @login_required FROM HERE (ONLY FIX)
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, "Invalid credentials or not staff")

    return render(request, "admin_login.html")

# Admin Logout
@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('/')

# Dashboard Home
@login_required(login_url='admin_login')
def dashboard_home(request):
    today = timezone.now().date()

    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(available=True).count()
    total_bookings = Booking.objects.count()
    active_bookings = Booking.objects.filter(check_out__gte=today).count()
    total_customers = User.objects.filter(is_staff=False).count()

    total_revenue = Booking.objects.filter(payment_status='paid').aggregate(
        total=Sum('total_price')
    )['total'] or 0

    revenue_today = Booking.objects.filter(
        payment_status='paid',
        created_at__date=today
    ).aggregate(total=Sum('total_price'))['total'] or 0

    checkins_today = Booking.objects.filter(check_in=today).count()
    checkouts_today = Booking.objects.filter(check_out=today).count()

    recent_bookings = Booking.objects.all().order_by('-created_at')[:10]

    context = {
        'today': today,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'total_customers': total_customers,
        'total_revenue': total_revenue,
        'revenue_today': revenue_today,
        'checkins_today': checkins_today,
        'checkouts_today': checkouts_today,
        'recent_bookings': recent_bookings,
        'current_customers': active_bookings
    }

    return render(request, 'dashboard.html', context)


# Rooms Page
@login_required(login_url='admin_login')
def rooms_detail(request):
    rooms = Room.objects.all()
    return render(request, 'dash_room.html', {'rooms': rooms})


# Bookings Page
@login_required(login_url='admin_login')
def bookings_detail(request):
    bookings = Booking.objects.all()
    return render(request, 'booking_list.html', {'bookings': bookings})


# Customers Page
@login_required(login_url='admin_login')
def customers_detail(request):
    customers = User.objects.all()

    customer_data = []

    for user in customers:
        bookings = Booking.objects.filter(user=user)

        total_bookings = bookings.count()
        total_spent = bookings.aggregate(total=Sum('total_price'))['total'] or 0

        customer_data.append({
            'id': user.id,
            'name': user.username,
            'email': user.email,
            'phone': '',
            'total_bookings': total_bookings,
            'total_spent': total_spent,
            'join_date': user.date_joined,
            'status': 'Active' if user.is_active else 'Inactive'
        })

    return render(request, "customer_list.html", {"customers": customer_data})


# Payments Page
@login_required(login_url='admin_login')
def payment_dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at')

    total_paid = Booking.objects.filter(payment_status='paid').aggregate(
        Sum('total_price')
    )['total_price__sum'] or 0

    pending = Booking.objects.filter(payment_status='pending').aggregate(
        Sum('total_price')
    )['total_price__sum'] or 0

    total_revenue = Booking.objects.aggregate(
        Sum('total_price')
    )['total_price__sum'] or 0

    monthly_data = (
        Booking.objects
        .filter(payment_status='paid')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('total_price'))
        .order_by('month')
    )

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    revenue_dict = {i: 0 for i in range(1, 13)}

    for entry in monthly_data:
        month_number = entry['month'].month
        revenue_dict[month_number] = float(entry['total'])

    months_list = months
    totals_list = [revenue_dict[i] for i in range(1, 13)]

    return render(request, "payment_dash.html", {
        "bookings": bookings,
        "total_paid": total_paid,
        "pending": pending,
        "total_revenue": total_revenue,
        "months": months_list,
        "totals": totals_list,
    })