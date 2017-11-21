# ORM

## 三步改变model
1. 修改models.py
2. python manage.py makemigrations [APP]创建改变的迁移文件，APP可选
3. python manage.py migrate 应用这些改变到DB

查看migrations文件的操作，不会执行，打印他的SQL语句：

    $ python manage.py sqlmigrate polls 0001

## 一对多，多对多

 ```
 from django.db import models

class Reporter(models.Model):
    # ...
    pass

class Article(models.Model):
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
 ```
 上面的例子，reporter.article_set可以访问一个reporter关联的多个文章。

 ```
 class Topping(models.Model):
    # ...
    pass

class Pizza(models.Model):
    toppings = models.ManyToManyField(Topping)
 ```
这个多对多的例子，方法可以作用于topping.pizza_set 以及pizza.toppings。

## 字段查找 field lookups
构建SQL的WHERE表达式时使用，作为QuerySet的fielter，exclude和get方法的参数。

    格式：field__lookuptype=value，双下划线

    >>> Entry.objects.filter(pub_date__lte='2006-01-01')

对应的SQL语句:

    SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';


# 项目
检查项目问题，不会生成migrations也不会碰数据库：

    $ python manage.py check

## 交互shell
如果要使用ipython作为交互的terminal，先安装ipython。

$ python manage.py shell

```
In [3]: Question.objects.all()
Out[3]: <QuerySet [<Question: What's up?>]>

In [4]: Question.objects.filter(question_text__startswith='What')
Out[4]: <QuerySet [<Question: What's up?>]>
```

# Django Admin

