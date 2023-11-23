from django.urls import path

from . import views  #означает каталог/модуль, в котором находится текущий файл.

urlpatterns = [ 
    path('', views.index, name='index'),
    path('buy/', views.conc_price, name='buy'),
    path('post_buy/', views.post_buy, name='post_buy'),
    
    # path('buy/<int:product_id>/', views.PurchaseCreate.as_view(template_name="shop/purchase_form.html"), name='buy'),
]
