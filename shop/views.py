from django.shortcuts import render #Чтобы из функции-представления передать данные в шаблон применяется третий параметр функции render(#при рендеренге передаем список продуктов контекст
        #передать данные в шаблон index.html), который еще называется context и который представляет словарь.
from django.http import HttpResponse  #отправка ответа клиенту, из него берется request
#from django.views.generic.edit import CreateView #отображает форму для создания объекта, повторно отображает форму с ошибками проверки и сохраняет объект в базу данных

from .models import Product, Purchase

# class PurchaseCreate(CreateView):
#      model = Purchase
#      fields = ['product', 'person', 'address', 'price']
#      template_name="shop/purchase_form.html"
#         # Переопределяем используемый шаблон

#      def form_valid(self, form): #из самого джанго, там определено/  form_valid() сохраняет форму, а затем перенаправляет на URL-адрес
#          self.object = form.save()
#          return HttpResponse(f'Спасибо за покупку, {self.object.person}!')


# Create your views here.
def index(request): 
    products = Product.objects.all()
    context = {'products': products} 
    return render(request, 'shop/index.html', context) 
        #браузер считывает эту строку и отображает пользователю страницу, составленную из этой разметки

def conc_price(request):# мы не знаем какой продукт берем
  
    promokod_new = request.POST.get('promokod_new') 
    
    if promokod_new is None:
        product_id = request.GET.get('product_id') #это срабаотывает, когда мы переходим по ссылке 
    else:
        product_id= request.POST.get('product_ID')  #срабатывает, когда применили промокод и отправляем данные на сервер

    productStr = Product.objects.get(pk = product_id) #строка выбранного товара
    discount_price = productStr.price
    if promokod_new == "new5":
        discount_price=discount_price-discount_price*0.05
    elif promokod_new == "new10":
         discount_price=discount_price-discount_price*0.1
    elif promokod_new == "new15":
         discount_price=discount_price-discount_price*0.15
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