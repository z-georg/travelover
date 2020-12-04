from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from accounts.models import UserProfileInfo
from core.core_functions import delete_old_image
from . import forms

# Create your views here.
from .forms import CommentPhotoForm, CreatePhotoForm, DeletePhotoForm, DeleteComment, EditComment
from .models import Photo, Comment, Like



def all_photos(request):
    current_user = request.user


    photos_list = Photo.objects.order_by('title')


    photos_dict = {'photos': photos_list,
                   'profile': current_user,
                   }
    return render(request, 'travel/photos_list.html', context=photos_dict)

def photo_details(request, pk):
    current_user = request.user

    photos_list = Photo.objects.get(pk=pk)
    photos_list.see_edit_and_delete_button = photos_list.user.user_id == request.user.id


    comment_list = Comment.objects.all()
    for el in comment_list:
            el.see_buttons = el.user.user_id == request.user.id
            if el.see_buttons:
                pass

    already_liked = True if len(Like.objects.filter(photo=photos_list)) > 0 else False

    if request.method == "GET":


        photos_dict = {'photos_list': photos_list,
                        'form': CommentPhotoForm(),
                       'comment_list': comment_list,
                       'already_liked': already_liked,
                       'profile': current_user,
                       }
        return render(request, 'travel/photo_details.html', context=photos_dict)
    else:
        form = CommentPhotoForm(request.POST)
        if form.is_valid():
            comment = Comment(comment=form.cleaned_data['comment'])
            comment.photo = photos_list
            comment.user = UserProfileInfo.objects.get(user=request.user)
            comment.user.id = UserProfileInfo.objects.get(user=request.user.id)

            comment.see_buttons = False
            if comment.photo.user.user_id == request.user.id:
                comment.see_buttons = True
            comment.save()
            print(comment)
            print(comment.photo.user.user_id)
            print(request.user.id)

            photos_list.save()

        context = {'photos_list': photos_list,
                   'form': CommentPhotoForm(),
                   'profile': current_user,}

        return render(request, 'travel/photo_details.html', context=context)

def create_photo(request):
    current_user = request.user

    if request.method == "GET":
        form = forms.CreatePhotoForm(request.GET)
        context = {'profile': current_user, }
        context.update({'form': form})

        return render(request, 'travel/create_photo.html', context=context)
    elif request.method == "POST":
        form = forms.CreatePhotoForm(request.POST, request.FILES)

        if form.is_valid():
            print("VALIDATION SUCCESS")
            photos_list = Photo.objects.order_by('title')
            photos_dict = {'photos': photos_list,
                           'profile': current_user,}

            new_photo = form.save()
            new_photo.user = UserProfileInfo.objects.get(user=request.user)
            new_photo.user.id = UserProfileInfo.objects.get(user=request.user.id)
            new_photo.save()

            print(new_photo)
            return render(request, 'travel/photos_list.html', context=photos_dict)




def edit_photo(request, pk):
    photos_list = get_object_or_404(Photo, pk=pk)
    current_user = request.user


    if request.method == "GET":
        form = CreatePhotoForm(instance=photos_list)
        context = {'profile': current_user, }
        context.update({'form': form})

        return render(request, 'travel/edit_photo.html', context=context)


    elif request.method == "POST":

     #   old_image = photos_list.image_url
        form = CreatePhotoForm(request.POST, request.FILES, instance=photos_list)
        if form.is_valid():
      #      if old_image:
       #         delete_old_image(old_image.path)
            photos_list = form.save(commit=False)
            photos_list.save()

        return redirect(f'http://127.0.0.1:8000/photos/details/{pk}')

    #  return render(request, 'travel/photo_details.html', context=context)
    context = {'photos_list': photos_list,
               'form': CommentPhotoForm()}
   # return redirect(reverse('photo_details', photos_list.pk))
    return render(request, 'travel/photo_details.html', context=context)

def delete_photo(request, pk):
    current_user = request.user

    photos_list = get_object_or_404(Photo, pk=pk)

    if request.method == "GET":
        form = DeletePhotoForm(instance=photos_list)
        context = {'profile': current_user, }
        context.update({'form': form})

        return render(request, 'travel/delete_photo.html', context=context)


    elif request.method == "POST":

        photos_list.delete()
        return redirect('http://127.0.0.1:8000/photos')


def like(request, pk):

    photo = Photo.objects.get(pk=pk)
    like = Like()
    like.photo = photo
    like.user = UserProfileInfo.objects.get(user=request.user)
    like.user.id = UserProfileInfo.objects.get(user=request.user.id)

    like.save()


    likes_of_current_user = 0
    for x in Like.objects.filter(photo=photo):
        if x.user.id == request.user.userprofileinfo.pk:
            likes_of_current_user += 1

    print(Like.objects.first().user.id == request.user.userprofileinfo.pk)

    print(f"likes_of_current_user {likes_of_current_user}")
    if like.user.id == request.user.userprofileinfo.pk:
        print("Dasdsa")
        print(like)
        if likes_of_current_user > 1:
            pass
            like.delete()
        else:
            pass


    photos_list = get_object_or_404(Photo, pk=pk)
    photos_dict = {'photos_list': photos_list,
                    "pk": pk,
                    'form': CommentPhotoForm(),
                    }
    return redirect(f'http://127.0.0.1:8000/photos/details/{pk}')
    # return redirect('pet_details', pk)
    #return HttpResponseRedirect(reverse('photo_details', args=(pk, )))
    #return redirect('http://127.0.0.1:8000/photos', id=pk)

    #return render(request, 'travel/photo_details.html', context=photos_dict)



#def comment(request, pk):
 #   print("Dsadasdsa")
  #  if request.method == "GET":


   #     form = CommentPhotoForm()
    #    return render(request, 'travel/edit_comment.html', {'form': form})
    #elif request.method == "POST":

     #   form = CommentPhotoForm(request.POST)
      #  if form.is_valid():
       #     photos_list = get_object_or_404(Photo, pk=pk)
        #    photos_dict = {'photos_list': photos_list}
         #   comment = form.save(commit=False)
          #  comment.photo = comment
           # comment.user = UserProfileInfo.objects.get(user=request.user)
            #comment.user.id = UserProfileInfo.objects.get(user=request.user.id)
            #comment.save()
        #    print(comment.user)
         #   return render(request, 'travel/photo_details.html', context=photos_dict)


def edit_comment(request, pk):
    current_user = request.user

    comments_list = get_object_or_404(Comment, pk=pk)
    pk_of_current_photo = comments_list.photo.pk

    if request.method == "GET":
        form = EditComment(instance=comments_list)
        context = {'profile': current_user, }
        context.update({'form': form})

        return render(request, 'travel/edit_comment.html', context=context)


    elif request.method == "POST":
        form = EditComment(request.POST, instance=comments_list)
        if form.is_valid():
            comments_list = form.save(commit=False)
            comments_list.save()

            return redirect(f'http://127.0.0.1:8000/photos/details/{pk_of_current_photo}')


def delete_comment(request, pk):
    current_user = request.user

    comments_list = get_object_or_404(Comment, pk=pk)
    pk_of_current_photo = comments_list.photo.pk

    if request.method == "GET":
        form = DeleteComment(instance=comments_list)
        context = {'profile': current_user, }
        context.update({'form': form})

        return render(request, 'travel/delete_comment.html', context=context)


    elif request.method == "POST":

        comments_list.delete()

        return redirect(f'http://127.0.0.1:8000/photos/details/{pk_of_current_photo}')




def all_photos_of_user(request, pk):
    current_user = request.user
    photo = get_object_or_404(Photo, pk=pk)
    owener_of_photo_username = photo.user
    owner_of_photo = photo.user.user_id
    filtered_all_photos = []
    all_photos = Photo.objects.all()
    for el in all_photos:
        if el.user.user_id == owner_of_photo:
            filtered_all_photos.append(el)

    context = {'photos_of_user': filtered_all_photos,
               'profile': current_user,
               'owner_of_photo_username': owener_of_photo_username,}

    return render(request, 'travel/photos_of_user.html', context=context)


