from django.urls import path
from . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from travel.views import CreatePhotoView, UpdatePhotoView, DeletePhotoView

app_name = 'travel'
urlpatterns = [
    url(r'^create/$', CreatePhotoView.as_view(), name = 'create'),
    url(r'^photos/$', views.all_photosListView.as_view(), name = 'all_photos'),
    path('photos/details/<int:pk>/',views.photo_details, name='photo_details'),
    path('edit/<int:pk>/', UpdatePhotoView.as_view(), name = 'edit_photo'),
    path('delete/<int:pk>/', DeletePhotoView.as_view(), name = 'delete_photo'),
    path('photos/like/<int:pk>/', views.like, name = 'like'),
    path('photos/edit_comment/<int:pk>/',views.edit_comment, name='edit_comment'),
    path('photos/delete_comment/<int:pk>/',views.delete_comment, name='delete_comment'),
    path('photos/details/<int:pk>/photos_of_user/',views.all_photos_of_user, name='photos_of_user'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)