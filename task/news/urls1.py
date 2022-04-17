from django.urls import path
from .views import PostList,PostSearch, PostDetailView, \
    PostCreateView, PostUpdateView, PostDeleteView, CategoryList, IndexView
# импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым,
    # позже станет ясно, почему
    #path('', PostsList.as_view()),
    # т. к. сам по себе это класс, то нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view
    #path('<int:pk>', PostDetail.as_view()),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='news_detail'), # ссылка на конкретную новость
    path('create/', PostCreateView.as_view(), name='news_create'),#ссылка на создание новости
    path('create/<int:pk>', PostUpdateView.as_view(), name='news_update'), #ссылка на редактирование новости
    path('delete/<int:pk>', PostDeleteView.as_view(), name='news_delete'), # ссылка на удаление новости
    path('search/', PostSearch.as_view(), name='news_search'),
    path('abonent/', CategoryList.as_view(), name='abonent_category'),
    path('test/', IndexView.as_view()),  # страница для тестирования Celery

]
