from django.urls import path
from . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import LogoutView

app_name = 'accounts'
urlpatterns = [

    url(r'^register/$', views.register, name = 'register'),
    url(r'^user_login/$', views.user_login, name = 'user_login'),
    url(r'^user_logout/$', LogoutView.as_view(), name = 'user_logout'),
    path('profile/<int:pk>/', views.my_profile, name= 'my_profile'),
    path('profile/delete_all_my_photos', views.delete_all_my_photos, name= 'delete_all_my_photos'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)