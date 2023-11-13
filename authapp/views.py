from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # You can add a redirect or a success message here
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'authapp/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'authapp/profile.html')