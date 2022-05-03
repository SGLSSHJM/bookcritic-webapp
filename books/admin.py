from django.contrib import admin
from .models import Book,Remark,User,Chat
# Register your models here.
admin.site.register(Book)
admin.site.register(Remark)
admin.site.register(User)
admin.site.register(Chat)
