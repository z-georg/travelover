from django.forms import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from accounts.models import UserProfileInfo
from . import forms, models

# Create your views here.
from .forms import CommentPhotoForm, CreatePhotoForm, DeletePhotoForm, DeleteComment, EditComment
from .models import Photo, Comment, Like


#def all_photos(request):
#    current_user = request.user

#    photos_list = Photo.objects.order_by('title')

#    photos_dict = {'photos': photos_list,
#                  'profile': current_user,
#                   }
#    return render(request, 'travel/photos_list.html', context=photos_dict)



class all_photosListView(ListView):

    model = models.Photo
    template_name = 'travel/photos_list.html'

    def get_context_data(self, **kwargs):
        photos_list = Photo.objects.order_by('title')

        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        context['photos'] = photos_list
        return context


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
            photos_list.save()

        context = {'photos_list': photos_list,
                   'form': CommentPhotoForm(),
                   'profile': current_user, }

        return render(request, 'travel/photo_details.html', context=context)


#def create_photo(request):
#    current_user = request.user
#
#    if request.method == "GET":
#        form = forms.CreatePhotoForm(request.GET)
#        context = {'profile': current_user, }
#        context.update({'form': form})
#
#        return render(request, 'travel/create_photo.html', context=context)
#    elif request.method == "POST":
#        form = forms.CreatePhotoForm(request.POST, request.FILES)
#
#        if form.is_valid():
#           print("VALIDATION SUCCESS")
#          photos_list = Photo.objects.order_by('title')
#         photos_dict = {'photos': photos_list,
#                           'profile': current_user, }
#
#            new_photo = form.save()
#            new_photo.user = UserProfileInfo.objects.get(user=request.user)
#            new_photo.user.id = UserProfileInfo.objects.get(user=request.user.id)
#            new_photo.save()
#           return render(request, 'travel/photos_list.html', context=photos_dict)



class CreatePhotoView(CreateView):
    template_name = 'travel/create_photo.html'
    model = Photo
    form_class = CreatePhotoForm

    def get_success_url(self):
        url = 'http://127.0.0.1:8000/photos/'
        return url

    def form_valid(self, form):
        new_photo = form.save(commit=False)
        new_photo.user = UserProfileInfo.objects.get(user=self.request.user)
        new_photo.user.id = UserProfileInfo.objects.get(user=self.request.user.id)
        new_photo.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        photos_list = Photo.objects.order_by('title')

        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        context['photos'] = photos_list
        return context

def edit_photo(request, pk):
    photos_list = get_object_or_404(Photo, pk=pk)
    current_user = request.user

    if request.method == "GET":
        form = CreatePhotoForm(instance=photos_list)
        context = {'profile': current_user, }
        context.update({'form': form})

        return render(request, 'travel/edit_photo.html', context=context)


    elif request.method == "POST":

        form = CreatePhotoForm(request.POST, request.FILES, instance=photos_list)
        if form.is_valid():
            photos_list = form.save(commit=False)
            photos_list.save()

        return redirect(f'http://127.0.0.1:8000/photos/details/{pk}')

    context = {'photos_list': photos_list,
               'form': CommentPhotoForm()}
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

    if like.user.id == request.user.userprofileinfo.pk:

        if likes_of_current_user > 1:
            pass
            like.delete()
        else:
            pass

    return redirect(f'http://127.0.0.1:8000/photos/details/{pk}')


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
    owner_of_photo_username = photo.user
    owner_of_photo = photo.user.user_id
    filtered_all_photos = []
    all_photos = Photo.objects.all()
    for el in all_photos:
        if el.user.user_id == owner_of_photo:
            filtered_all_photos.append(el)

    context = {'photos_of_user': filtered_all_photos,
               'profile': current_user,
               'owner_of_photo_username': owner_of_photo_username, }

    return render(request, 'travel/photos_of_user.html', context=context)