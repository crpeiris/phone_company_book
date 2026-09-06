from django.http import HttpResponseNotFound
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from store.models import Profile, Order
from .forms import SignUpForm
from django import forms

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
# Create your views here.

# For Dashboard
from django.urls import reverse
from django.apps import apps


def login_user(request):
    if not request.method == "POST":
        return render( request, 'user_accounts/login.html', {'title': 'Sign in'})
    
    elif request.method == "POST":
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, ("You have been Logged in..."))
            return redirect ('storehome')
        else:
            messages.error(request, ("Username or Password incorrect...Please try again"))
            return redirect ('login_user')


def logout_user(request):
    logout(request)
    messages.success(request, ('Logged out...Thank you!'))
    return redirect('storehome')


def register_user(request):
    form = SignUpForm()
    if not request.method == "POST":
        return render(request,'user_accounts/register.html', {'form': form, 'title': 'Join with us'})


    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data["username"]
            password= form.cleaned_data["password1"]
            #log in user
            user =authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("You have registered! Welcome !!!"))
            return redirect('welcome')
        else:
            messages.error(request, ("threre is a problem registering, try agaian"))
            return redirect('register_user')
    
def welcome(request):
    return render(request, 'user_accounts/welcome.html',{'title': 'Welcome to Future Phoneshop'})


@login_required(login_url='login_user')
def userprofile(request):
    try:
        userprofile = Profile.objects.get(user=request.user)
        return render(request, 'user_accounts/userprofile.html', {'userprofile': userprofile, 'title': "User Profile"})
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('welcome')


@login_required(login_url='login_user')
def edit_userprofile_image(request):
    if request.method == 'POST':
        userprofile = Profile.objects.get(user=request.user)
        if 'image' in request.FILES:
            userprofile.image = request.FILES['image']
            userprofile.save()
            messages.success(request, "Profile image updated successfully.")
        else:
            messages.error(request, "No image provided.")
        return redirect('edit_userprofile')
    else:
        return redirect('userprofile')
    
@login_required(login_url='login_user')
def edit_userprofile_details(request):
    if request.method == 'POST':
        userprofile = Profile.objects.get(user=request.user)
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        
        # Update additional profile fields
        userprofile.phone = request.POST.get('phone', userprofile.phone)
        userprofile.address1 = request.POST.get('address1', userprofile.address1)
        userprofile.address2 = request.POST.get('address2', userprofile.address2)
        userprofile.city = request.POST.get('city', userprofile.city)
        userprofile.state = request.POST.get('state', userprofile.state)
        userprofile.country = request.POST.get('country', userprofile.country)
        userprofile.zipcode = request.POST.get('zipcode', userprofile.zipcode)
        userprofile.save()
        
        messages.success(request, "Profile details updated successfully.")
        return redirect('edit_userprofile')
    else:
        return redirect('userprofile')


@login_required(login_url='login_user')
def edit_userprofile(request):
    try:
        userprofile = Profile.objects.get(user=request.user)
        return render(request, 'user_accounts/edit_userprofile.html', {'userprofile': userprofile, 'title': "Edit User Profile"})
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('welcome')


@login_required(login_url='login_user')
def change_password(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('oldPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')


        # Check if the old password is correct
        if check_password(old_password, user.password):
            # Ensure the new password and confirmation match
            if new_password == confirm_password:
                try:
                    # Validate the new password
                    password_validation.validate_password(new_password, user)
                    
                    # If valid, set the password
                    user.set_password(new_password)
                    user.save()
                    
                    # Keep the user logged in after the password change
                    update_session_auth_hash(request, user)
                    
                    messages.success(request, "Password changed successfully.")
                    return redirect('userprofile')
                except ValidationError as e:
                    # Catch validation errors and display them to the user
                    for error in e:
                        messages.error(request, error)
            else:
                messages.error(request, "New password and confirmation do not match.")
        else:
            messages.error(request, "Old password is incorrect.")


        return redirect('change_password')
    else:
        return render(request, 'user_accounts/change_password.html', {'title': "Change Password"})


#For Dashboard

@login_required
def model_dashboard(request):
    """Fetches all models and evaluates user permissions for each action."""
    models_data = []
    user = request.user  # Get currently logged-in user
    
    for model in apps.get_models():
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        
        # ==================== NEW: PERMISSION CHECKS ====================
        is_staff = user.is_staff
        can_create = is_staff and user.has_perm(f"{app_label}.add_{model_name}")
        can_edit   = is_staff and user.has_perm(f"{app_label}.change_{model_name}")
        can_delete = is_staff and user.has_perm(f"{app_label}.delete_{model_name}")
        can_view   = is_staff and user.has_perm(f"{app_label}.view_{model_name}")
        # =================================================================

        models_data.append({
            'app_label': app_label,
            'model_name': model_name,
            'verbose_name': model._meta.verbose_name.title(),
            'app_name': model._meta.app_config.verbose_name,
            
            # ==================== NEW: PASS FLAGS TO TEMPLATE ====================
            'can_create': can_create,
            'can_edit': can_edit,
            'can_delete': can_delete,
            'can_view': can_view,
            # =====================================================================
        })
    
    models_data = sorted(models_data, key=lambda x: (x['app_name'], x['verbose_name']))
    return render(request, 'user_accounts/dashboard.html', {'models': models_data})


@login_required
def model_action_proxy(request, app_label, model_name, action):
    """Fallback proxy view to enforce security if a disabled link is manually accessed."""
    perm_action = action
    if action == 'edit':
        perm_action = 'change'
    elif action == 'create':
        perm_action = 'add'
        
    perm_string = f"{app_label}.{perm_action}_{model_name}"
    
    if not (request.user.is_staff and request.user.has_perm(perm_string)):
        return render(request, 'user_accounts/no_rights.html', {
            'action': action.title(), 
            'model': model_name.title()
        })

    try:
        if action == 'create':
            url = reverse(f"admin:{app_label}_{model_name}_add")
        else:
            url = reverse(f"admin:{app_label}_{model_name}_changelist")
        return redirect(url)
        
    except Exception:
        return render(request, 'user_accounts/no_rights.html', {
            'custom_message': f"The model '{model_name.title()}' is not registered in the Django Admin interface."
        })