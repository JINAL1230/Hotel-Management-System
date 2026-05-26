from django.shortcuts import render, get_object_or_404, redirect
from rooms.models import Room
from .models import Booking
from django.contrib.auth.decorators import login_required
from decimal import Decimal

@login_required
def booking(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        check_in = request.POST.get("checkin")
        check_out = request.POST.get("checkout")
        total_price = request.POST.get("total")

        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        guests = request.POST.get("guests")
        requests_text = request.POST.get("requests")

        # Safe convert total price
        try:
            total_price = Decimal(total_price)
        except:
            total_price = room.price

        # Validation
        if not check_in or not check_out or not fname or not email:
            return render(request, "booking.html", {
                "room": room,
                "error": "Please fill all required fields"
            })

        # SAVE DATA ✅
        Booking.objects.create(
            user=request.user,
            room=room,

            check_in=check_in,
            check_out=check_out,

            guests=guests or 1,

            first_name=fname,
            last_name=lname,
            email=email,
            phone=phone,

            special_requests=requests_text,

            total_price=total_price,

            payment_status='paid',  # or 'pending'
            status='pending'
        )

        return redirect("booking_success")

    return render(request, "booking.html", {"room": room})


def booking_success(request):
    return render(request, "booking_success.html")