from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from travel.models import Photo
from . import forms
# Create your views here.
from accounts.forms import UserForm, UserProfileInfoFrom, LoginForm
from accounts.models import UserProfileInfo


# Create your views here.

@transaction.atomic
def register(request):

    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoFrom(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)

            print(user)
            print(user.password)

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print("successss")
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            print(profile.profile_pic.url)

            registered = True
            login(request, user)
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoFrom()


    return render(request, 'accounts/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered}
                  )


def user_login(request):
    if request.method == "GET":
        return render(request, 'accounts/login.html', {'login_form': LoginForm()})

    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            #user = login_form.save()

            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            #  Use set_password here
           # user.set_password(password)
            #user.save()
            user = authenticate(username=username, password=password)
            print(password)

            print(user)

            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('http://127.0.0.1:8000')
                else:
                    return HttpResponseRedirect("ACCOUNT NOT ACTIVE")
            else:
                print("User tried to login and failed!")
                return HttpResponse("invalid login details!")

@login_required
def user_logout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000')




def my_profile(request, pk):
    current_user = get_object_or_404(User, pk=pk)
    user_info = UserProfileInfo(user_id=pk)
    user_picture = user_info.profile_pic
    print(current_user)
    print(f"piiic: {user_info.profile_pic}")
    photos_list = Photo.objects.order_by('title')
    filtered_photo_list = []
    for photo in photos_list:
        if photo.user == UserProfileInfo.objects.get(user=request.user):
            filtered_photo_list.append(photo)
    user_picture.user = User.objects.get(id=pk)
    user_picture.user.id = UserProfileInfo.objects.get(user=request.user.id)


    if request.method == "GET":
        form = UserProfileInfoFrom()

        user_dict = {'profile': current_user,
                     'photos': filtered_photo_list,
                     'form': form}


        return render(request, 'accounts/my_profile.html', user_dict)
    elif request.method == "POST":

        print("POST")

        form = UserProfileInfoFrom(request.POST, request.FILES, instance=current_user.userprofileinfo)
        if form.is_valid():

            user_info = form.save(commit=False)
            user_info.save()





            user_dict = {'profile': current_user,
                         'picture': user_picture,
                         'photos': filtered_photo_list,
                         'form': form}

            return render(request, 'accounts/my_profile.html', user_dict)

        user_dict = {'profile': current_user,
                     'picture': user_picture,
                     'photos': filtered_photo_list,
                     'form': form}

        return render(request, 'accounts/my_profile.html', user_dict)


def delete_all_my_photos(request):
        current_user = request.user
        all_my_photos = Photo.objects.all()
        filtered_all_my_photos = []
        for el in all_my_photos:
            if el.user.user_id == request.user.id:
                filtered_all_my_photos.append(el)

        if request.method == "GET":
            return render(request, 'accounts/delete_all_my_photos.html', context={'profile': current_user})

        elif request.method == "POST":
            for photo in filtered_all_my_photos:
                photo.delete()

            return render(request, 'accounts/my_profile.html', context={'profile': current_user})
           # return redirect(f'http://127.0.0.1:8000')
