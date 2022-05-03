from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Remark,User
from . import models
from . import forms
from django.template import loader
from django.shortcuts import redirect
import hashlib

# Create your views here

def home(request):
        return redirect("index")

def index(request):
    if not request.session.get('is_login', None):
        return redirect('login')
    return render(request, 'books/index.html', {
        "books": Book.objects.all(),
    })
def remark(request, remark_id):
    response = "You are looking at the %s remark."  
    return HttpResponse(response % remark_id)
def bookdetail(request, book_id):
    book=Book.objects.get(pk=book_id)
    remark_list=book.remark_set.all()
    return render(request, 'books/bookdetail.html', {
        "book":book, "remarks": remark_list,
    })

def addremark(request):
    remarktext = request.GET["remark_text"]
    score_number = request.GET["score"]
    username = request.session['user_name']
    book_name1 = request.GET["bookname"]
    selectedbook = Book.objects.get(book_name = book_name1)
    book_id = selectedbook.pk
    new_remark = Remark(user = username, book=selectedbook, score = score_number, remark_text = remarktext)
    new_remark.save()
    return bookdetail(request, book_id)

def create(request):
    if request.method == "POST":
        m = Book()
        m.book_name = request.POST["create_name"]
        m.author_name = request.POST["create_author"]
        m.desc = request.POST["create_desc"]
        m.image_url = request.POST["img_url"]
        m.save()
        return redirect("index")
    return render(request, "books/create.html")

def login(request):
    if request.session.get('is_login',None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)       
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'books/login.html', locals())
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('index')
            else:
                message = '密码不正确！'
                return render(request, 'books/login.html', locals())
        else:
            return render(request, 'books/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'books/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('index')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'books/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'books/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'books/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('login')
        else:
            return render(request, 'books/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'books/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("login")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("login")
    
def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def author_list(request):
    author_list = Book.objects.values('author_name').distinct()
    return render(request, "books/authorlist.html",{
        "author_list" : author_list,
    })


def theauthor(request):
    authorname=request.GET["author_name"]
    author_books = Book.objects.filter(author_name = authorname)
    message = authorname
    return render(request, "books/index.html",{
        "books" : author_books,"message" : message,
    })

