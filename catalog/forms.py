from django import forms

from catalog.models import Product, Version


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('date_of_creation', 'last_modified_date', 'author')

    def clean_name(self):
        """
        Выдает ошибку при наличии запрещенных слов в строковом значении поля "name"
        """
        cleaned_data = self.cleaned_data['name'].lower()
        stop_list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for i in stop_list:
            if i in cleaned_data:
                raise forms.ValidationError('Недопустимое название')
        return cleaned_data

    def clean_description(self):
        """
        Создает список слов разделенных пробелом.
        Выдает ошибку при точном совпадении слова из списка со словом из списка запрещенных слов.
        """
        cleaned_data = self.cleaned_data['description'].lower()
        description_list = cleaned_data.split()
        for i in description_list:
            if i in ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']:
                raise forms.ValidationError('Недопустимое описание')
        return cleaned_data


class VersionForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = "__all__"
