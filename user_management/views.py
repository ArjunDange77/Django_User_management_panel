from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('user_list') 
        else:
            error_message = "Invalid username or password."
            return render(request, 'user_management_panel/login.html', {'error_message': error_message})
    else:
        return render(request, 'user_management_panel/login.html')

@login_required
def user_list(request):
    try:
        users = User.objects.filter(userprofile__is_soft_deleted=False).order_by('-id')
        paginator = Paginator(users, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'user_management_panel/user_list.html', {'users': users, 'page_obj': page_obj})
    except:
        error_message = "Login to view this page "
        return render(request, 'user_management_panel/login.html', {'error_message': error_message})



@login_required
def user_create(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save(commit=False)
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()

            return redirect('user_list')
        else:
            return JsonResponse({'status': 'error', 'errors': user_form.errors})
    else:
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        return render(request, 'user_management_panel/user_create.html', {'user_form': user_form, 'user_profile_form': user_profile_form})


@login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        user_profile_form = UserProfileForm(request.POST, instance=user.userprofile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return redirect('user_list')
        else:
            return JsonResponse({'status': 'error', 'errors': user_form.errors})
    else:
        user_form = UserForm(instance=user)
        user_profile_form = UserProfileForm(instance=user.userprofile)
        return render(request, 'user_management_panel/user_update.html', {'user_form': user_form, 'user_profile_form': user_profile_form, 'user': user})


@login_required
@require_POST
def user_soft_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = user.userprofile
    user_profile.is_soft_deleted = True
    user_profile.save()
    return redirect('user_list')







