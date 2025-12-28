from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Account
from .models import Appointment
from django.contrib import messages

def doctor_list(request):
    doctors = Account.objects.filter(is_doctor=True, is_active=True)   
    context = {
        'doctors': doctors,    }
    return render(request, 'doctor/doctor_list.html', context)
from django.contrib.auth.decorators import login_required





@login_required(login_url='login')
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Account, user_id=doctor_id, is_doctor=True) 
    if request.method == 'POST':
        date = request.POST.get('appointment_date')
        prescription = request.FILES.get('prescription') 
        message = request.POST.get('message')



        Appointment.objects.create(
            user=request.user, 
            doctor=doctor, 
            appointment_date=date,
            prescription=prescription,
            message=message
        )
        messages.success(request, 'Appointment booked successfully!')
        return redirect('doctor_list')

    return render(request, 'doctor/book_appointment.html', {'doctor': doctor})