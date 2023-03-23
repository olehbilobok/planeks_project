import datetime
from django.contrib.auth.models import User
from django.db import models


COLUMN_SEPARATOR_CHOICES = (
    (0, ';'),
    (1, ','),
)

STRING_CHARACTER_CHOICES = (
    (0, "'"),
    (1, '"'),
)

COLUMN_TYPE_CHOICES = (
    (0, 'Full name'),
    (1, 'Job'),
    (2, 'Email'),
    (3, 'Domain name'),
    (4, 'Phone number'),
    (5, 'Company name'),
    (6, 'Text'),
    (7, 'Integer'),
    (8, 'Address'),
    (9, 'Date'),
)


class Schema(models.Model):

    id = models.AutoField(primary_key=True)
    schema_name = models.CharField(max_length=50)
    column_separator = models.IntegerField(choices=COLUMN_SEPARATOR_CHOICES, default=1)
    string_character = models.IntegerField(choices=STRING_CHARACTER_CHOICES, default=1)
    created_at = models.DateTimeField(editable=False, auto_now=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=datetime.datetime.now())
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schemas')

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    def __str__(self):
        return f"id: {self.id}, name: {self.schema_name}"


class Column(models.Model):

    id = models.AutoField(primary_key=True)
    column_name = models.CharField(max_length=50)
    type = models.IntegerField(choices=COLUMN_TYPE_CHOICES)
    order = models.IntegerField()
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name='columns')

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    def __str__(self):
        return f"id: {self.id}, name: {self.column_name}, type={self.type}, order={self.order}"

    def to_dict(self):
        return {
            'id': self.id,
            'column_name': self.column_name,
            'type': self.type,
            'order': self.order,
            'schema': self.schema
             }
