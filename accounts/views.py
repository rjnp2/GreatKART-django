from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#send mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_no = form.cleaned_data['phone_no']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(first_name= first_name, last_name=last_name,
                     username=username,email=email,password=password)
            user.phone_no = phone_no
            user.save()

            #user activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'

            message = render_to_string('account/account_verfication_user.html',
                        { 'user': user,
                        'domain': current_site ,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user)
                        }) 
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect('/account/login/?command=verification&email='+email)

    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'account/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')

        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'account/signin.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged Out')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation, Your account is activated')
        return redirect('login')
    
    else:
        messages.error(request, 'Invalid login credentials')
        return redirect('register')

@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'account/dashboard.html')

def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST['email']

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #forget password mail
            current_site = get_current_site(request)
            mail_subject = 'Please change your password'

            message = render_to_string('account/forget_password_email.html',
                        { 'user': user,
                        'domain': current_site ,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user)
                        }) 
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Reset link send to email')
            return redirect('forgetpassword')

        else:
            messages.error(request, 'Wrong email Account')
            return redirect('forgetpassword')
    return render(request, 'account/forgetpassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetpassword')

    else:
        messages.error(request, 'This link has been expired')
        return redirect('login')

def resetpassword(request):

    if request.method == 'POST':
        password = request.POST['password']
        conform_password = request.POST['conform_password']

        if password == conform_password:
            uid = request.session['uid']
            user = Account.objects.get(pk=uid)

            user.set_password(password)
            user.save()
            
            messages.success(request, 'Successfully reset password')
            return redirect('login')

        else:
            messages.error(request, 'Password and conform password doesnot match')
            return redirect('resetpassword')

    else:
        return render(request, 'account/resetpassword.html')