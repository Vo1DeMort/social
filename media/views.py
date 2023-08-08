from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, ProfileEditForm
from . models import Profile


# it's working
# but it's intended to be a news feed ,so gotta build some more upon this
# this is not finished yet
def home (request):
    if request.user.is_authenticated:
        return render(request,'home.html')
    else:
        return redirect('login')

    # if the user is not login ,should be redirected to login page


# check the registeration views  ,coz login is failing to authenticate the user created form the registeration form
# not finished yet
# {{ next }} !!
def login_user(request):
    if request.method == 'POST':
        # instantiated from forms, this form is form ,not model form
        # means manual data processing and persistance is required
        form = LoginForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['username'],pasthe sword

            # both username and password is stored in cd
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])

            # means if the user exists
            if user is not None:
                # check if the user is active and allowed to login and perform certain actions with the system 
                if user.is_active:
                    # simply login the user
                    login(request, user)
                    messages.success(request,('login success'))
                    return redirect('home')
                else:
                    return redirect('login')
            else:
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
	logout(request)
	messages.success(request, ("logout success"))
	return redirect('home')


# now it's working properly ,well done
def register_user(request):
    if request.method == 'POST':
        user_form = SignupForm (request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            # set_password: from user model
            # do the password hasing
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            # no need to user signals anymore
            Profile.objects.create(user=new_user)
            '''what i want is if the regiserration is success ,the user will be login and redirect to home '''
            auth_user = authenticate(
                request,username= new_user.username,password = user_form.cleaned_data['password']
            )
            # this will redirect the user to home page ,coz i design so
            # that design( login_user ) won't take effect in this func ,gotta redirect like so
            if auth_user:
                login(request,auth_user)
        return redirect('home')
            
    else:
        user_form = SignupForm()

    return render(request,
                  'register.html',
                  {'user_form': user_form})

# retrieving related profile is success logically ,awesome
# it's not complete just yet
@login_required(login_url='login')
def profile_page(request):
    profile = Profile.objects.get(user=request.user)

    return render(request,'profile.html',{'profile':profile})

def user_post(request):
    pass 


    """
    ERROR : solved ,wtf is action in template ,that's what i messed with to have the error
    """
@login_required
def edit_profile(request):
    user = Profile.objects.get(user=request.user.id)
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=user)
    if request.method =='POST':
        # there is a pontensial error , i haven't installed pillow 
        if form.is_valid():
            form.save()
            messages.success(request,('Updating success'))
            return redirect('profile')
    else :
        messages.success(request,('plz login'))

    return render (request,'edit_profile.html',{'form':form})
    
    



