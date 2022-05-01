from django.urls import path
from . import views





urlpatterns = [
    path('', views.index, name='index'),
    path('remark/<int:remark_id>', views.remark, name='remark'),
    path('detail/<int:book_id>', views.bookdetail, name="bookdetail"),
]
