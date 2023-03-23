from django.contrib import admin
from schema.models import Schema, Column


class SchemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'schema_name', 'column_separator', 'string_character', 'created_at', 'updated_at', 'user')


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('id', 'column_name', 'type', 'order')


admin.site.register(Schema, SchemaAdmin)
admin.site.register(Column, ColumnAdmin)
