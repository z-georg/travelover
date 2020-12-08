from django.shortcuts import render


# Create your views here.
from django.views.generic.base import TemplateView


#def index(request):
#    current_user = request.user
#    return render(request, 'common/index.html', context={'profile': current_user, })


class IndexView(TemplateView):
    template_name = 'common/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        return context

