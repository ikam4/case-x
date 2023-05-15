from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    money = models.FloatField(default=0)
    ref_code = models.CharField(max_length=30)
    inventory = models.TextField()
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Skins(models.Model):
    skin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    image = models.FileField(upload_to='main/static/img')
    price = models.FloatField()
    quality = models.CharField(max_length=30)
    class Meta:
        verbose_name = "Скин"
        verbose_name_plural = "Скины"


class History(models.Model):
    user_id = models.CharField(max_length=30)
    skin = models.CharField(max_length=30)
    coef = models.FloatField()
    time = models.DateTimeField()
    class Meta:
        verbose_name = "История"
        verbose_name_plural = "Истории"

class Case(models.Model):
    name = models.CharField(max_length=30)
    image = models.FileField(upload_to='main/static/img')
    price = models.FloatField()
    items = models.TextField()
    class Meta:
        verbose_name = "Кейс"
        verbose_name_plural = "Кейсы"

class Support(models.Model):
    user_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    problem = models.TextField()
    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"