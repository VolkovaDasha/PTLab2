from django.test import TestCase, Client
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
