from django.db import models

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.CharField(max_length=150, verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}, {self.description}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.CharField(max_length=150, verbose_name='описание')
    preview = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(verbose_name='Категория', to='Category', on_delete=models.DO_NOTHING)
    purchase_price = models.IntegerField(verbose_name='цена за покупку')
    date_of_creation = models.DateTimeField(verbose_name='дата создания', **NULLABLE)
    last_modified_date = models.DateTimeField(verbose_name='дата последнего изменения', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)

    def get_active_version(self):
        data = Version.objects.all().filter(product=self.pk, is_active=True).last()
        if data:
            return f'{data.version_name} - {data.version_number}'


class Version(models.Model):
    product = models.ForeignKey(verbose_name='Продукт', to='Product', on_delete=models.CASCADE)
    version_number = models.IntegerField(verbose_name='номер версии', **NULLABLE)
    version_name = models.CharField(max_length=150, verbose_name='Название версии', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активная версия', **NULLABLE)

    def __str__(self):
        return f'{self.version_name} {self.version_number} ({self.product})'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
