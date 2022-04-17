from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post, Category, User


# studes = Student.objects.filter(courses__name="Algebra")
# блок рассылки подписчикам уведомления о новом сообщении
#@receiver(post_save, sender=Post)
@receiver(m2m_changed, sender=Post.category_post.through)
#def notify_managers_appointment(sender, instance, created, **kwargs):
def notify_managers_appointment(sender, instance, action, **kwargs):
    id_post = instance.id
    id_post_cat = instance.postcategory_set.all()
    if action == "post_add":
        print('создалась новая статья')
        print('***************Рассылка*******************')
        print(id_post, id_post_cat)
        print(id_post_cat.all().values('category'))
        for id_cat in id_post_cat.all().values('category'):
            id_cat
        mail_adres=Category.objects.get(id=id_cat['category'])
        print(mail_adres.abonent.all())
        if mail_adres.abonent.all():
            print('Подписки есть')
            for adres in mail_adres.abonent.all():
                # print (adres.email)
                # print(f'Новая статья в категории ->> {mail_adres}')
                # print(f'Ссылка на статью ->> http://127.0.0.1:8000/newsall/{id_post}')
                send_mail(
                    subject=f'Новая статья в категории ->> {mail_adres}',
                    message=f'Ссылка на статью ->> http://127.0.0.1:8000/newsall/{id_post}',
                    from_email='Umba.dog@yandex.ru',
                    recipient_list=[adres.email],
                )
        else:
            print('Подписок нет')
        print('***************Рассылка*******************')

# сигнал создания нового юзера
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    pass
    if created:
       print('Создан новый юзер')
       print(instance.username)
       print(instance.email)
       send_mail(
           subject=f'Регистрация на новостном портале нового пользователя ->> {instance.username}',
           message=f'Приветствуем Вас {instance.username} на сайте новостного портала',
           from_email='Umba.dog@yandex.ru',
           recipient_list=[instance.email],
       )

