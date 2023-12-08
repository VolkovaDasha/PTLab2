[![Build Status](https://app.travis-ci.com/kpdvstu/PTLab2.svg?branch=master)](https://app.travis-ci.com/kpdvstu/PTLab2)
# Лабораторная 2 по дисциплине "Технологии программирования"
Лабораторная работа № 2
Изучение фреймворка MVC
Цели работы:
1. Познакомиться c моделью MVC, ее сущностью и основными фреймворками на ее основе.
2. Разобраться с сущностями «модель», «контроллер», «представление», их функциональным 
назначением.
3. Получить навыки разработки веб-приложений с использованием MVC-фреймворков, написания 
модульных тестов к ним.

![image](https://github.com/VolkovaDasha/PTLab2/assets/118906106/fab9ab8c-14e8-4c56-876b-bfb06ce5ea9e)

### измененный файл проекта views.py

```from django.shortcuts import render
from django.http import HttpResponse  
#from django.views.generic.edit import CreateView

from .models import Product, Purchase

def index(request): 
    products = Product.objects.all()
    context = {'products': products} 
    return render(request, 'shop/index.html', context) 
        #браузер считывает эту строку и отображает пользователю страницу, составленную из этой разметки

def conc_price(request):# мы не знаем какой продукт берем
  
    promokod_new = request.POST.get('promokod_new') 
    
    if promokod_new is None:
        product_id = request.GET.get('product_id')
    else:
        product_id= request.POST.get('product_ID')  
    productStr = Product.objects.get(pk = product_id) 
    discount_price = productStr.price
    if promokod_new == "new5":
        discount_price=int(discount_price-discount_price*0.05)
    elif promokod_new == "new10":
         discount_price=int(discount_price-discount_price*0.1)
    elif promokod_new == "new15":
         discount_price=int(discount_price-discount_price*0.15)
    else: discount_price = discount_price
    contexts = {'ProductsStr': productStr,'product_ID': product_id, 'promokod_new':promokod_new, 'discount_price':discount_price}
    return render(request, 'shop/purchase_form.html', contexts)

def post_buy(request):
    product_id = request.POST.get('product_id')
    person = request.POST.get('person')
    address = request.POST.get('address')
    price = request.POST.get('price')

    product = Product.objects.get(pk = product_id)

    purchase = Purchase(product=product, person = person, address=address, price=price)
    purchase.save()
    return HttpResponse(f'Спасибо за покупку, {person}!')
```
### измененный файл проекта urls.py

```from django.urls import path

from . import views  #означает каталог/модуль, в котором находится текущий файл.

urlpatterns = [ 
    path('', views.index, name='index'),
    path('buy/', views.conc_price, name='buy'),
    path('post_buy/', views.post_buy, name='post_buy'), 
]
```
### измененный файл проекта purchase_form.html
```<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width" />
    <title>Покупка</title>
</head>
<body>
    <div>
        <h3>Покупка</h3>
        <form id = "promokods" method="post" action="/buy/">{% csrf_token %}
            <input type="hidden" value="{{ product_ID }}" name="product_ID" />
            <table> 
                <tr>
                    <td><p>Вы выбрали: </p></td>
                    <td><p>{{ ProductsStr.name }}</p></td>
                </tr>
                <tr>
                    <td><p>Цена: </p></td>
                    <td><p> {{ ProductsStr.price}}</p></td>
                </tr>
            
                <tr>
                    <td><p>Введите промокод </p></td>
                    <td><input type="text" name="promokod_new" /> </td>
                 </tr>
                 <tr><td><input type="submit", form ="promokods", value="Применить промокод" /> </td></tr>
            </table>
        </form>


        <form id="purchase" method="post" action="/post_buy/">{% csrf_token %}
            <input type="hidden" value="{{ product_ID }}" name="product_id" />
            
           
            <table>
                <tr>
                    <td><p>Введите свое имя </p></td>
                    <td><input type="text" name="person" /> </td>
                </tr>
                <tr>
                    <td><p>Введите адрес доставки:</p></td>
                    <td>
                        <input type="text" name="address" />
                    </td>
                </tr>
                <tr>
                    <td><p>К оплате:</p></td>
                    <td>
                        <input type="number" readonly value="{{discount_price}}" name="price" />
                    </td>
                </tr>
                <tr><td><input type="submit", form ="purchase", value="Отправить" /> </td><td></td></tr>
            </table>
        </form>
    </div>
</body>
</html>
```

### измененный файл проекта models.py
``` from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField(default=0)
```
### измененный файл проекта test_views.py
``` from django.test import TestCase, Client
#from shop.views import PurchaseCreate
from shop.models import Product



class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webpage_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class ConcPriceTestCase(TestCase):
    def setUp(self):
        self.clients = Client()
        self.product = Product.objects.create(name="book", price="740")

    def test_conc_price_GET(self):
        response = self.clients.get(f'/buy/?product_id={self.product.pk}')
        self.assertEqual(response.status_code, 200)

    def test_conc_price_POST(self):

        form_data = {'promokod_new':'new10',
                     'product_ID': self.product.pk}
        responce = self.clients.post ('/buy/',data=form_data)
      
        self.assertInHTML(needle='<input type="number" readonly value="666.0" name="price" />', haystack=responce.content.decode('utf-8'))
        self.assertTemplateUsed(responce,'shop/purchase_form.html')

class Test_post_buy(TestCase):

    def setUp(self):
        self.clients = Client()
        self.product = Product.objects.create(name="book", price="740")
        self.person = 'Ivanov'
    def test_post_buy(self):
        
        form_data = {'person':self.person, 
                     'address':'Svetlaya St.',
                     'price':self.product.price,
                     'product_id': self.product.pk}

        response = self.client.post('/post_buy/',data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(f'Спасибо за покупку, {self.person}!', response.content.decode('utf-8'))
```
### измененный файл проекта test_views.py
``` from django.test import TestCase
from shop.models import Product, Purchase
from datetime import datetime

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="book", price="740")
        Product.objects.create(name="pencil", price="50")

    def test_correctness_types(self):                   
        self.assertIsInstance(Product.objects.get(name="book").name, str)
        self.assertIsInstance(Product.objects.get(name="book").price, int)
        self.assertIsInstance(Product.objects.get(name="pencil").name, str)
        self.assertIsInstance(Product.objects.get(name="pencil").price, int)        

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="book").price == 740)
        self.assertTrue(Product.objects.get(name="pencil").price == 50)


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product_book = Product.objects.create(name="book", price="740")
        self.datetime = datetime.now()
        Purchase.objects.create(product=self.product_book,
                                person="Ivanov",
                                address="Svetlaya St.",
                                price=self.product_book.price)

    def test_correctness_types(self):
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).person, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).address, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).date, datetime)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).price, int)
        

    def test_correctness_data(self):
        self.assertTrue(Purchase.objects.get(product=self.product_book).person == "Ivanov")
        self.assertTrue(Purchase.objects.get(product=self.product_book).address == "Svetlaya St.")
        self.assertTrue(Purchase.objects.get(product=self.product_book).date.replace(microsecond=0) == \
            self.datetime.replace(microsecond=0))
        self.assertEqual(Purchase.objects.get(product=self.product_book).price, 740)
```

### Вывод
В ходе лабораторной работы познакомились с моделью MVC, ее сущностью и основными фреймворками на ее основе и функциональным назначением каждой сущности. Получили навыки разработки веб-приложений с использованием MVC-фреймворков и написания 
модульных тестов к ним.





