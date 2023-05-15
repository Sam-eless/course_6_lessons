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
        return f'{self.name}, {self.description}, {self.preview}, {self.category},' \
               f'{self.purchase_price}, {self.date_of_creation}, {self.last_modified_date}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)
