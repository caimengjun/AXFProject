from django.conf.urls import url

from app import views

urlpatterns = [
    url(r"^home/",views.home,name="home"),
url(r"^market/",views.market,name="market"),
url(r"^marketWithParm/(\d+)/(\d+)/(\d+)",views.marketWithParm,name="marketWithParm"),
url(r"^cart/",views.cart,name="cart"),
url(r"^mine/",views.mine,name="mine"),
url(r"^register/",views.register,name="register"),
url(r"^login/",views.login,name="login"),
url(r"^logout/",views.logout,name="logout"),
url(r"^addToCart/",views.addToCart,name="addToCart"),
url(r"^subToCart/",views.subToCart,name="subToCart"),
url(r"^iscunzai/",views.iscunzai,name="iscunzai"),

url(r"^addCartNum/",views.addCartNum,name="addCartNum"),
url(r"^subCartNum/",views.subCartNum,name="subCartNum"),
url(r"^changeSelectStatu/",views.changeSelectStatu,name="changeSelectStatu"),
url(r"^changeManySelectStatu/",views.changeManySelectStatu,name="changeManySelectStatu"),
url(r"^createOrder/",views.createOrder,name="createOrder"),
url(r"^orderInfo/(.+)",views.orderInfo,name="orderInfo"),
    url(r"^checkUserUnique/", views.checkUserUnique, name="checkUserUnique"),
    url(r"^changeOrderStatu/", views.changeOrderStatu, name="changeOrderStatu"),
]
