from django.shortcuts import render,redirect
from .forms import RegisterCustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model

# Create your views here.
User = get_user_model()

def register_customer(request):
    user = None
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True
            user.username = user.email
            user.save()
            messages.success(request,'Account created successfully. Please login')
            return redirect('accounts:login')
        else:
            messages.warning(request,'Oops, something went wrong. Please try again')
            return redirect('accounts:register-customer')
    else:
        form = RegisterCustomerForm()
        return render(request,'accounts/register-customer.html',{'form':form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None and user.is_active:
            login(request,user)
            return redirect('dashboard:dashboard')
        else:
            messages.warning(request,'Oops, something went wrong. Please try again')
            return redirect('accounts:login')
    else:
        return render(request,'accounts/login.html')
    
def logout_user(request):
    logout(request)
    messages.success(request,'Active session ended. Log in to continue')
    return redirect('accounts:login')

def change_password(request):
    pass

def update_profile(request):
    pass

