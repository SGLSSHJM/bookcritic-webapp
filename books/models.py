from django.db import models

# Create your models here.
class Book(models.Model):
    book_name = models.CharField(max_length=50)
    author_name = models.CharField(max_length=30)
    desc = models.TextField(default="暂无简介") 
    image_url = models.CharField(max_length=228, default = None, blank = True, null = True)
    def __str__(self):
        return self.book_name





class Remark(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.IntegerField()
    remark_text = models.CharField(max_length=500)
    def __str__(self):
        return self.remark_text