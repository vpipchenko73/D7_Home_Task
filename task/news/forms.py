from django.forms import ModelForm, BooleanField
from .models import Post, Category

# сщздаем модельную форму

class PostForm(ModelForm):
    check_box=BooleanField(label='Подтвердите')
    # в класс мета заносим модель и нужные нам поля
    class Meta:
        model=Post
        fields=['title', 'text', 'autor','category_post','check_box']


