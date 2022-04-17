import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
# импорт  компонентов для еженедельной рассылки
from news.models import Post, Category, User, PostCategory, CategoryUser
from datetime import datetime, timedelta
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


# https://pypi.org/project/django-apscheduler/ ссылка на документацию
# наша задача по выводу текста на экран
def my_job():
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."  # в командную строку вводить  -->> python manage.py runapscheduler

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(week="*/1"),  # Время повторения задачи 1 одна неделя
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"
                                ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            # max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")


