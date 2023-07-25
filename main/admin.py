from django.contrib import admin
from main.models import News, Category, Tag, Comment

# Register your models here.

admin.site.register(News)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
