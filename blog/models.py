from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое', **NULLABLE)
    slug = models.CharField(verbose_name='URL', max_length=255, blank=True, unique=True)
    preview = models.ImageField(upload_to='posts/', verbose_name='изображение', default="posts/nophoto.png")
    date_of_creation = models.DateTimeField(default=now, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликована ли статья?')
    number_of_views = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.title}'

    def delete(self, *args, **kwargs):
        self.is_published = False
        self.save()

    def increment_count_view(self):
        self.number_of_views += 1
        self.save()

        if self.number_of_views == 100:
            # Указать почту на которую будет приходить письмо.
            email = ('default@default.com',)
            send_mail(
                'Достижение',
                f'Поздравляю, Ваша статья - "{self.title}" набрала 100 просмотров!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=email,
            )

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ('-date_of_creation',)
