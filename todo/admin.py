from django.contrib import admin

from todo.models import Todo


@admin.register(Todo) # admin.site.register(Todo)와 같다.
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id','name','todo')