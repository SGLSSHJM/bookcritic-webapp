from django.urls import path
from . import views





urlpatterns = [
    path('index', views.index, name='index'),
    path('remark/<int:remark_id>', views.remark, name='remark'),
    path('detail/<int:book_id>', views.bookdetail, name="bookdetail"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),
    path('addremark', views.addremark, name="addremark"),
]
