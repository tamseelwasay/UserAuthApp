from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser  # Import your custom user model

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until it is verified
            user.save()

            # Email sending logic
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('authapp/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('authapp:account_activation_sent')  # Redirect to a confirmation page
    else:
        form = UserRegisterForm()
    return render(request, 'authapp/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)  # Use CustomUser instead of User
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):  # Catch CustomUser.DoesNotExist
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'authapp/account_activation_success.html')
    else:
        return render(request, 'authapp/account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'authapp/account_activation_sent.html')


@login_required
def profile(request):
    return render(request, 'authapp/profile.html')