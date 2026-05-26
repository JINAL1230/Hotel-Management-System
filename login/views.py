from django.shortcuts import render, redirect

def login_page(request):
    if request.method == "POST":
        return redirect('thank_you')   # no validation

    return render(request, 'login.html')


def thank_you(request):
    return render(request, 'thankyou.html')