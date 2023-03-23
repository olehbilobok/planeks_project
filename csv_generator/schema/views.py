import re
import os
from django.http import JsonResponse
from django.shortcuts import render, redirect
from schema.models import Schema, Column
from schema.forms import ColumnForm, SchemaForm, SchemaUpdateForm, ColumnUpdateForm
from schema.utils import CSVManager
from django.http import HttpResponse, Http404


def get_schema(request):
    context = {}
    schema = Schema.objects.filter(user=request.user).all()
    context['data'] = schema
    return render(request, 'schemas.html', context)


def create_schema(request):
    context = {}
    redirect_url = 'http://127.0.0.1:8000/schema/generate'

    if request.method == "POST":
        schema_name = request.POST.getlist('schema_name[]')
        column_separator = request.POST.getlist('column_separator[]')
        string_character = request.POST.getlist('string_character[]')
        column_name = request.POST.getlist('column_name[]')
        type = request.POST.getlist('type[]')
        order = request.POST.getlist('order[]')

        if '' in schema_name or '' in column_separator or '' in string_character or '' in column_name \
                or '' in type or '' in order:
            return JsonResponse({'schema_error': 'All fields are required '})
        else:

            schema = Schema.objects.filter(user=request.user).filter(schema_name=schema_name[0])
            if schema:
                return JsonResponse({'schema_error': 'This schema name is already in use'})

            post_data = {
                'schema_name': schema_name[0],
                'column_separator': column_separator[0],
                'string_character': string_character[0],
                'user': request.user
            }

            form = SchemaForm(post_data)
            if form.is_valid():
                new_schema = form.save()

                post_data = []
                dataset = zip(column_name, type, order)
                for collect in tuple(dataset):
                    post_data.append(
                        {
                            'column_name': collect[0],
                            'type': collect[1],
                            'order': int(collect[2]),
                            'schema': new_schema
                        }
                    )
                for column in post_data:
                    column_form = ColumnForm(column)
                    if column_form.is_valid():
                        column_form.save()
                return JsonResponse({'redirect_url': redirect_url})

    if request.method == "GET":
        form = SchemaForm()
        column_form = ColumnForm()
        context['schema_form'] = form
        context['column_form'] = column_form

    return render(request, 'create_schema.html', context)


def generate_data(request):
    context = {}
    schemas = Schema.objects.filter(user=request.user).order_by('-created_at')
    last_schema = schemas.first()
    columns = last_schema.columns.order_by('order')

    if request.method == 'POST':

        CSVManager(last_schema, request.POST.get('rows')).file_writer()

    context['data_column'] = columns
    context['data_schema'] = schemas
    context['last_schema'] = last_schema

    return render(request, 'generate_data.html', context)


def edit_schema(request, pk):
    context = {}
    schema = Schema.objects.filter(id=pk).first()
    columns = schema.columns.order_by('order')
    redirect_url = 'http://127.0.0.1:8000/schema/generate'

    if request.method == 'POST':
        schema_name = request.POST.getlist('schema_name[]')
        column_separator = request.POST.getlist('column_separator[]')
        string_character = request.POST.getlist('string_character[]')
        column_name = request.POST.getlist('column_name[]')
        type = request.POST.getlist('type[]')
        order = request.POST.getlist('order[]')

        if '' in schema_name or '' in column_separator or '' in string_character or '' in column_name \
                or '' in type or '' in order:
            return JsonResponse({'schema_error': 'All fields are required '})

        if len(order) != len(set(order)):
            return JsonResponse({'schema_error': 'All fields must have unique order'})

        post_data = {
            'schema_name': schema_name[0],
            'column_separator': column_separator[0],
            'string_character': string_character[0],
            'user': request.user
        }

        form = SchemaUpdateForm(post_data, instance=schema)
        if form.is_valid():
            form.initial = post_data
            new_schema = form.save()

            post_data = []
            dataset = zip(column_name, type, order)
            for collect in tuple(dataset):
                post_data.append(
                    {
                        'column_name': collect[0],
                        'type': collect[1],
                        'order': int(collect[2]),
                        'schema': new_schema
                    }
                )
            list_columns = list(columns).copy()
            for column in post_data:
                column_form = ColumnUpdateForm(column, instance=list_columns.pop(0) if list_columns else None)
                if column_form.is_valid():
                    column_form.initial = column
                    column_form.save()
            return JsonResponse({'redirect_url': redirect_url})

    if request.method == 'GET':
        form = SchemaUpdateForm(
            initial=
            {

                'schema_name': schema.schema_name,
                'column_separator': schema.column_separator,
                'string_character': schema.string_character,
            }
        )

        columns_lst = []
        for column in columns:
            columns_lst.append(ColumnUpdateForm(
                initial=
                {
                    'id': column.id,
                    'column_name': column.column_name,
                    'type': column.type,
                    'order': column.order,
                    'schema': column.schema.id
                }
            )
            )
        context['schema_form'] = form
        context['column_form'] = columns_lst
        context['column_form_empty'] = ColumnUpdateForm()
        context['id'] = pk

    return render(request, 'edit_schema.html', context)


def delete_column(request, column_pk, schema_pk):

    column = Column.objects.get(id=column_pk)
    column.delete()

    return redirect('edit_schema', pk=schema_pk)


def download_file(request, schema_name):
    file_name = request.user.username + '_' + schema_name + '.csv'
    file_path = os.path.abspath(f'schema/media/{file_name}')
    if file_path:
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

