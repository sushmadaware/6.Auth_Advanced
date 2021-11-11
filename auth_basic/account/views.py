from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http import HttpResponse, BadHeaderError
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignupForm

# Create your views here.
def home(request):
    template_name='account/base.html'
    context={}
    return render(request,template_name,context)

def loginview(request):
    if request.method=='POST':
        u=request.POST.get('uname')
        p= request.POST.get('pw')
        user=authenticate(username=u,password=p)
        print(user)
        if user is not None:
            login(request,user)
            return HttpResponse('login successful')
        else:
            messages.error(request,'Invalid Credentials')
    template_name='account/log_in.html'
    context={}
    return render(request,template_name,context)


def logoutview(request):
    logout(request)
    return redirect('login')


def registerview(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            user_email=form.cleaned_data.get('email')
            messages.success(request,f'Account created for {username}!')
            send_mail(
                'Account Created',
                'Your Account has created succesful',
                'dawaresushma@gmail.com',
                [user_email],
                fail_silently=False
            )
            return redirect('login')
    template_name='account/register.html'
    context={'form':form}
    return render(request,template_name,context)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "account/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'dawaresushma@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("home")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="account/password_reset.html", context={"password_reset_form":password_reset_form})











