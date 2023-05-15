from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name= 'index'),
    path('support/', views.support, name= 'support'),
    path('my_acc/', views.my_acc, name= 'my_acc'),
    path('register/', views.register, name= 'register'),
    path('login/', views.login, name= 'login'),
    path('faq/', views.faq, name= 'faq'),
    path('exit/', views.exit, name= 'exit'),
    path('api/get_case_items', views.get_case_items, name= 'get_case_items'),
    path('api/buy_case', views.buy_case, name= 'buy_case'),
    path('api/inv_add_item', views.inv_add_item, name= 'inv_add_item')
]
