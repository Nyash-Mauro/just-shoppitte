from django.shortcuts import render, redirect
from . models import *
from .forms import *
from django.contrib.auth.decorators import login_required




def home(request):
 = Item.objects.all()
    return render(request, 'award/index.html', {"items": Items})


@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = itemUpload(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()
        return redirect('home')
    else:
        form = itemUpload()
        return render(request, 'award/new_post.html', {"form": form})


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            recipient = User(username=username, email=email)
            try:
                (request, f'Account has been created successfully!')
            except:
                print('error')
            return redirect('login')

    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/registration_form.html', context)


def search_project(request):

    if 'search' in request.GET and request.GET["search"]:

        search_term = request.GET.get("search")
        searched_project = Item.objects.filter(title__icontains=search_term)
        message = f"{search_term}"
        return render(request, 'award/search.html', {"message": message, "projects": searched_project})

    else:
        message = "You haven't searched for any term "
        return render(request, 'award/search.html', {"message": message})


@login_required(login_url='/accounts/profile/')
def update_profile(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
        return redirect('home')
    else:
        form = UpdateProfileForm(instance=request.user.profile)
        return render(request, 'award/update_profile.html', {'form': form})


def profile_info(request):

    current_user = request.user
    profile_info = Profile.objects.filter(user=current_user).first()
    projects = request.user.post_set.all()

    return render(request, 'award/profile.html', {"projects": projects, "profile": profile_info, "current_user": current_user})


