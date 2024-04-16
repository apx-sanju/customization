from django.contrib import messages

from django.contrib.auth.models import User 
# Importing the User model from Django's authentication system for user management.

from django.contrib.auth import authenticate, login,logout
# Importing authentication functions for user login and logout from Django's authentication system.

from .models import UserProfile# Importing the UserProfile model from the current directory's(users.models) models module.

from django.shortcuts import render, redirect
# Importing render and redirect functions from Django's shortcuts for handling view rendering and HTTP redirects.

from django.views.decorators.csrf import csrf_protect

import os,math,random,smtplib #for otp 

from product.models import Product
# Importing the Product model from the product app's models module for product management.


    
#-----------------------------------------------------------------------------------------------------------------------

# ---------------------Login View------------------------------------------#

# CSRF protection decorator for the sign-in view
@csrf_protect
def sign_in(request):
    
    # Check if the request method is GET
    if request.method == 'GET':
        # Render the login-registration.html template
        return render(request, 'login-register/login-registration.html')

    # If request method is not GET, i.e., it's POST
    else:
        # Retrieve username and password from the POST request
        username = request.POST['username']
        password = request.POST['userpassword']
        
        # Authenticate the user using the provided credentials
        user = authenticate(username=username, password=password)

        # If authentication is successful
        if user is not None:
            # Log in the user
            login(request, user)

            # Query the UserProfile associated with the logged-in user
            user_profile = UserProfile.objects.filter(user=request.user)

            # Prepare context data to be passed to the redirected view
            #context is a dictionary [user_profile_data is a : KEY and user_profile is : Value]
            context = {}
            context['user_profile_data'] = user_profile
            

            # Redirect the user to the index page
            return redirect("/index/")


#----------------------------------------------------------------------------------------------------------------

# ---------------------Registration View--------------------------------------------#

def sign_up(request):
    # Taking a Blank dictionary so it is usable in every syntax...
    context = {}
    
    # Check if the request method is GET
    if request.method == 'GET':
        # Render the login-registration.html template
        return render(request, 'login-register/login-registration.html')

    # If request method is POST
    elif request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['user_password']
        confirm_password = request.POST['user_confirm_password']

        # Check if any field is blank
        if name == '' or username == '' or password == '' or confirm_password == '':
            context['errmsg'] = 'Fields cannot be blank'
            return render(request, 'login-register/login-registration.html', context)

        # Check if password and confirm password match
        elif password != confirm_password:
            context['errmsg'] = 'Password and confirm password do not match'
            return render(request, 'login-register/login-registration.html', context)

        # Check if password is at least 8 characters long
        elif len(password) < 8:
            context['errmsg'] = 'Password must be at least 8 characters long'
            return render(request, 'login-register/login-registration.html', context)

        else:
            try:
                # Create a new user object
                user = User.objects.create(username=username)
                # Set the password for the user
                user.set_password(password)
                # Save the user object
                user.save()

                # If user object is created successfully
                if user is not None:
                    # Create a UserProfile object associated with the user
                    profile = UserProfile.objects.create(user=user, name=name, email=username)
                    # Save the profile object
                    profile.save()
                    
                    # Set success message
                    context['success'] = 'Successfully registered'
                    return render(request, 'login-register/login-registration.html', context)

                else:
                    # If user object creation fails
                    context['errmsg'] = "Unfortunately, User Profile could not be created"
                    return render(request, 'login-register/login-registration.html', context)
            
            except Exception as e:
                # Handle exceptions, such as duplicate user or other errors
                context['errmsg'] = "User already exists or an error occurred: {}".format(str(e))
                return render(request, 'login-register/login-registration.html', context)

#-------------------------------------------------------------------------------------------------------------

            
def user_logout(request):
    logout(request)
    return redirect('sign_up')

#-------------------------------------------------------------------------------------------------------------


#--------------------------------INDEX---------------------------------------------------------------#

def index(request):
    # Initialize user variable as None
    current_user = None
    
    # Check if the request user is authenticated
    if request.user.is_authenticated:
        # Retrieve UserProfile object associated with the authenticated user
        current_user = UserProfile.objects.filter(user=request.user)
    
    # Retrieve active product details to display on the index page
    active_products = Product.objects.filter(is_active=True)
    
    # Construct the context dictionary containing product details and user data
    context = {
        'product_details': active_products,  # Product details to display on the index page
        'user_data': current_user  # UserProfile data of the authenticated user, if available
    }
    
    # Render the index.html template with the constructed context
    return render(request, 'index.html', context)

#---------------------------------------------------------------------------------------------
#---------------------------------User Profile on Index page----------------------------#
def profile(request):
    # Retrieve UserProfile object associated with the authenticated user
    user_profile = UserProfile.objects.filter(user=request.user)
    
    # Retrieve UserProfile object associated with the authenticated user (can remove one of these)
    user_profile_duplicate = UserProfile.objects.filter(user=request.user)
    
    # Construct the context dictionary containing user profile data
    context = {
        'user_profile_data': user_profile,          # User profile data for display
        'user_profile_data_duplicate': user_profile_duplicate  # Duplicate user profile data (if needed)
    }
    
    # Render the profile.html template with the constructed context
    return render(request, 'profile.html', context)
