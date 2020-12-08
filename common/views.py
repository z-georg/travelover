from django.shortcuts import render


# Create your views here.


def index(request):
    current_user = request.user
    return render(request, 'common/index.html', context={'profile': current_user, })
