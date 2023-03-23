from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from schema.models import Schema, Column, COLUMN_SEPARATOR_CHOICES, STRING_CHARACTER_CHOICES


class SchemaForm(forms.ModelForm):
    column_separator = forms.ChoiceField(choices=COLUMN_SEPARATOR_CHOICES)
    string_character = forms.ChoiceField(choices=STRING_CHARACTER_CHOICES)

    class Meta:
        model = Schema
        fields = ('schema_name', 'column_separator', 'string_character', 'user')


class ColumnForm(forms.ModelForm):

    class Meta:
        model = Column
        fields = ('column_name', 'type', 'order', 'schema')


class SchemaUpdateForm(forms.ModelForm):
    column_separator = forms.ChoiceField(choices=COLUMN_SEPARATOR_CHOICES)
    string_character = forms.ChoiceField(choices=STRING_CHARACTER_CHOICES)

    class Meta:
        model = Schema
        fields = ('schema_name', 'column_separator', 'string_character', 'user')

    def clean_schema(self):
        if self.is_valid():
            schema_name = self.cleaned_data['schema_name']
            try:
                schema = Schema.objects.filter(pk=self.instance.pk).get(schema_name=schema_name)
            except ObjectDoesNotExist:
                return schema_name
            return JsonResponse({'schema_error': 'This schema name is already in use'})


class ColumnUpdateForm(forms.ModelForm):

    class Meta:
        model = Column
        fields = ('column_name', 'type', 'order', 'schema')

