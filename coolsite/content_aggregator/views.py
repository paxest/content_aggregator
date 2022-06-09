from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from .forms import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import ArticleSerializer
from .utils import *


class ContentHome(LoginRequiredMixin, DataMixin, ListView):
    model = Article
    template_name = 'content_aggregator/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        articles = Article.objects.all().select_related('category')
        ordering = self.request.GET.get('orderby')
        
        if ordering:
            articles = articles.order_by(ordering)
        return articles


    def get_context_data(self, *, object_list=None, **kwargs):
        print(*zip(['asd', 'qwe'], ['fg', 'wer']))
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))


class ContentCategory(LoginRequiredMixin, DataMixin, ListView):
    model = Article
    template_name = 'content_aggregator/index.html'
    context_object_name = 'articles'
    allow_empty = False

    def get_queryset(self):
        articles = Article.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True).select_related('category')
        ordering = self.request.GET.get('orderby')
        
        if ordering:
            articles = articles.order_by(ordering)
        return articles


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        c_def = self.get_user_context(title='Категория - ' + category.name,
                                      category_selected=category.id)
        return dict(list(context.items()) + list(c_def.items()))


class ArticleDetail(LoginRequiredMixin, DataMixin, DetailView):
    model = Article
    template_name = 'content_aggregator/article.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'].views += 1
        context['article'].save()
        c_def = self.get_user_context(title=context['article'])
        return dict(list(context.items()) + list(c_def.items()))


class RegistrationUser(DataMixin, CreateView):
    form_class = RegistrationUserForm
    template_name = 'content_aggregator/registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('create_user_categories')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'content_aggregator/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class UserCategoriesCreateView(LoginRequiredMixin, DataMixin, CreateView):
    model = UserProfile
    template_name = 'content_aggregator/create_user_categories.html'
    fields = ('user_category',)
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание профиля')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserCategoriesUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = UserCategoriesForm
    model = UserProfile
    template_name = 'content_aggregator/edit_user_categories.html'
    slug_field = "user__username"
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Мои категории')
        return dict(list(context.items()) + list(c_def.items()))


class UserProfileView(LoginRequiredMixin, DataMixin, DetailView):
    model = User
    template_name = 'content_aggregator/user_profile.html'
    slug_field = 'username'
    context_object_name = 'user_profile'
    
    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Профиль')
        return dict(list(context.items()) + list(c_def.items()))


class UserProfileUpdateView(DataMixin, UpdateView):
    form_class = UserProfileForm
    model = User
    template_name = 'content_aggregator/edit_user_profile.html'
    slug_field = "username"
   
    def get_success_url(self):
        print(self.kwargs)
        return reverse_lazy('user_profile', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение профиля')
        return dict(list(context.items()) + list(c_def.items()))


class APIView(DataMixin, TemplateView):
    template_name = 'content_aggregator/api.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='API')
        return dict(list(context.items()) + list(c_def.items()))


class AboutView(DataMixin, TemplateView):
    template_name = 'content_aggregator/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        return dict(list(context.items()) + list(c_def.items()))

def logout_user(request):
    logout(request)
    return redirect('login')


def about(request):
    return render(request, 'content_aggregator/about.html', {'menu': menu, 'title': 'О сайте'})


def show_api(request):
    return HttpResponse('API сайта')


def show_contacts(request):
    return HttpResponse('Контакты')


# API
class ArticleAPIList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)


class ArticleAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class ArticleAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAdminOrReadOnly,)
