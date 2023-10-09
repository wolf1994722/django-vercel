from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from authen.forms import SignUpForm
# Create your views here.


def home(request):
    return  render(request, 'auth/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', { 'form' : form })



# Now we dive into signup() function. It gets user data from HTTP POST request which is handled by SignUpForm, save user to database.

# Then we use authenticate() function and login() function from django.contrib.auth to log the user in.

# If the process is successful, redirect to homepage, otherwise, return to signup.html template.