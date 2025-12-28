from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required

from doctor.models import Doctor # Make sure to import this!

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user_role = request.POST.get('user_role') 
            is_doc = True if user_role == 'doctor' else False
            is_pat = True if user_role == 'patient' else False

            user = Account.objects.create_user(
                first_name=first_name, 
                last_name=last_name, 
                email=email,
                username=username,
                password=password,
                is_doctor=is_doc,
                is_patient=is_pat
            )
            user.phone_number = phone_number
            user.save()

            # --- NEW DOCTOR PROFILE LOGIC ---
            if is_doc:
                # Grab the extra data sent from the dropdown/inputs in register.html
                spec = request.POST.get('specialization')
                days = request.POST.get('available_days')
                time = request.POST.get('available_time')

                # Create the entry in the Doctor table linked to this User
                Doctor.objects.create(
                    user=user,
                    specialization=spec,
                    available_days=days,
                    available_time=time if time else "09:00:00" # fallback if empty
                )
            # --- END NEW LOGIC ---

            messages.success(request, 'Registration complete')
            return redirect('login')
    else:
        form = RegistrationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)
def login(request):
    if request.method== 'POST':
        email= request.POST['email']
        password = request.POST ['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            #messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')