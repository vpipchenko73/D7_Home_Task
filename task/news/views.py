# импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail

from django.views.generic import ListView, DetailView  # импортируем класс получения деталей объекта
from django.views.generic import UpdateView, CreateView, \
    DeleteView  # импортируем класс создания редактирования и удаления обьектов
from .models import Post, Category, User, PostCategory, CategoryUser
from .filters import PostFilter  # импортируем недавно написанный фильтр
from .forms import PostForm
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
# Celery test
from django.http import HttpResponse
from .tasks import hello, printer


# Новости
class PostList(ListView):
    model = Post
    template_name = 'newsall.html'
    context_object_name = 'newsall'
    # queryset = Post.objects.order_by('-dateCreation') # выводим статьи в обратном порядке
    ordering = ['-dateCreation']
    paginate_by = 10  # поставим постраничный вывод в 10 элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['value1'] = f"Все новости . общее количество новостей ->>{Post.objects.all().count()}"
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    # queryset = Post.objects.order_by('-dateCreation') # выводим статьи в обратном порядке
    ordering = ['-dateCreation']
    paginate_by = 10  # поставим постраничный вывод в 10 элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['value1'] = f"Все новости . общее количество новостей ->>{Post.objects.all().count()}"
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetailView(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'news_detail.html'  # название шаблона будет product.html
    # context_object_name = 'news_detail'  # название объекта. в нём будет
    queryset = Post.objects.all()


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news_create.html'
    form_class = PostForm


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'news_create.html'
    form_class = PostForm

    # делаем метод что бы получить информацию об объекте которы мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/newsall/'


# https://stackoverflow.com/questions/618557/django-using-select-multiple-and-post -получение всех полей модели
# блок подписки и рассылки уведомлений о подписке
class CategoryList(ListView):
    model = Category
    template_name = 'abonent_category.html'
    context_object_name = 'abonent_category'

    def post(self, request, *args, **kwargs):
        id_category = request.POST.getlist("Подписка")  # доделано что бы можно было несколько подписок оформлять сразу
        print(f'категория- {id_category} ')
        mass_cat=''
        for id_cat in id_category:
            #print (Category.objects.get(id=id_cat))
            #print (request.user)
            a=Category.objects.get(id=id_cat)
            a.abonent.add(request.user)
            mass_cat=mass_cat+f'{a}; '
        send_mail(
            subject=f'{request.user.username} Вы подписаны на статьи в категории {mass_cat}',
            message=f'{request.user.username} Вы подписаны на статьи в категории {mass_cat}',
            from_email='Umba.dog@yandex.ru',
            recipient_list=[request.user.email],
        )
        return redirect('/newsall/')


class IndexView(View):  # тестирование Celery
    def get(self, request):
        printer.apply_async([10], countdown = 5, expires=60)
        hello.delay()
        return HttpResponse('Hello!')



