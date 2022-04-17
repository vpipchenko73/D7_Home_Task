from celery import shared_task
import time
# импорт  компонентов для еженедельной рассылки
from news.models import Post, Category, User, PostCategory, CategoryUser
from datetime import datetime, timedelta
from django.core.mail import send_mail

#  тестирование Celery ##########################
@shared_task
def hello():
    #time.sleep(10)
    print("Hello, world!")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)
#################################################

# еженедельная рассылка новых статей подписчикам
@shared_task
def weekly_newsletter():
    #  Your job processing logic here...
    print('работает периодическая задача ')
    pull_post = {}  # словарь с выборкой необходимых к рассылке новостей - ключ - категория новости
    a = Post.objects.filter(dateCreation__range=[datetime.now() - timedelta(days=7), datetime.now()])
    for b in a:  # итерация Post
        for pc in b.postcategory_set.all():  # итерация транзитной категории PostCategory
            # print(pc.get_id_cat(),pc.get_id_post())
            # достаем с помощью функций модели PostCategory id category и id post
            pull_post[pc.get_id_cat()] = pull_post.get(pc.get_id_cat(), []) + [pc.get_id_post()]
            # формируем словарь category/post
    print(pull_post)
    # рассылка писем
    for cat in pull_post.keys():
        mail_adres = Category.objects.get(id=cat)
        if mail_adres.abonent.all():
            news = ''
            for post in pull_post[cat]:
                news = f'{news}* Новость -->> http://127.0.0.1:8000/newsall/{post}\n'
            # print(news)
        # формирование и рассылка писем
        if mail_adres.abonent.all():
            send_mail(
                subject=f'Пулл новых статей в категории ->> {mail_adres}',
                message=news,
                from_email='Umba.dog@yandex.ru',
                recipient_list=[ml.email for ml in mail_adres.abonent.all()],
            )
        else:
            print(f'На новые статьи в категории {mail_adres} нет подписки')
