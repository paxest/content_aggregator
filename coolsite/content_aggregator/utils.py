from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from .models import *


menu = [
    {'title': 'Главная', 'url_name': 'home', 'icon': '<i class="fa-solid fa-house"></i>'},
    {'title': 'О сайте', 'url_name': 'about', 'icon': '<i class="fa-solid fa-bars-staggered"></i>'},
    {'title': 'API', 'url_name': 'api', 'icon': '<i class="fa-solid fa-code"></i>'},
    {'title': 'Контакты', 'url_name': 'contacts', 'icon': '<i class="fa-solid fa-file-contract"></i>'},
    {'title': 'Админ', 'url_name': 'admin:index', 'icon': '<i class="fa-solid fa-gears"></i>'},
]


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        context['articles_count'] = Article.objects.all()
        user_menu = menu.copy()

        if not self.request.user.is_staff:
            user_menu.pop()
        context['menu'] = user_menu
        
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'userprofile'):
                context['user_categories'] = UserProfile.objects.get(user_id=self.request.user.id).user_category.annotate(Count('article'))
            if 'category_selected' not in context:
                context['category_selected'] = 0
        else:
            redirect('login')

        return context


class CurrentUserMixin(object):
    model = User

    def get_object(self, *args, **kwargs):
        try:
            obj = super(CurrentUserMixin, self).get_object(*args, **kwargs)
        except AttributeError:
            # SingleObjectMixin throws an AttributeError when no pk or slug
            # is present on the url. In those cases, we use the current user
            obj = self.request.user.username

        return obj
