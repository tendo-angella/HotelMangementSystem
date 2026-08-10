from django.shortcuts import render, redirect
from .models import Payment
from .forms import PaymentForm

# Create your views here.
def payment_list(request):
    # Fetch all payments, newest first
    payments = Payment.objects.all().order_by('-payment_date')
    return render(request, 'payment_list.html', {'payments': payments})


def record_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    
    return render(request, 'payment_form.html', {'form': form})
