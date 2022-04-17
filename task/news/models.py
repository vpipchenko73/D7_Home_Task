from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Autor(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    category_name = models.CharField(max_length=24)
    abonent = models.ManyToManyField(User, through='CategoryUser')

    def __str__(self):
        return f'{self.category_name}'

    def get_id_cat(self):
        return f'{self.id}'


class Post(models.Model):
    dateCreation = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=128)
    text = models.TextField()
    autor = models.ForeignKey(Autor, default='Нет автора', on_delete=models.CASCADE)
    category_post = models.ManyToManyField(Category, default='Без категории', through='PostCategory')
    rating = models.SmallIntegerField(default=0)

    # class Meta:
    #   ordering=['-dateCreation']

    def __str__(self):
        return f"{self.title[0:16]} / {self.text[0:128]}{'...'} Автор- {str(self.autor)}"

    def get_absolute_url(self):
        # return f'/newsall/{self.id}'
        return f'/newsall/'

    def get_id_url(self):
        return f'newsall/{self.id}'


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def get_id_cat(self):
        return f'{self.category.id}'

    def get_id_post(self):
        return f'{self.post.id}'


class CategoryUser(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
