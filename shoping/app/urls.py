from django.conf.urls import url, include
from django.contrib import admin

from app import views

urlpatterns = [
    url(r'^home/',views.home,name="home"),
    url(r'^market/$',views.market,name="market"),
    url(r'^cart/',views.cart,name="cart"),
    url(r'^mine/',views.mine,name="mine"),

    url(r'^market/(\d+)/(\d+)/(\d+)',views.marketWithParam,name="market_param"),
    url(r'^register/',views.register,name="register"),
    url(r'^checkUser/',views.checkUser), #检查用户名唯一性的
    url(r'^login/',views.login,name="login"),
    url(r'^logout/',views.loginOut,name="loginout"),
    url(r'^addToCart/',views.addToCart,name="addToCart"),
    url(r'^subToCart/',views.subToCart,name="subToCart"),
    url(r'^addCart/',views.addCart,name="addCart"),
    url(r'^subCart/',views.subCart,name="subCart"),
    url(r'^chanageSelect/',views.chanageSelect,name="chanageSelect"),
    url(r'^changeManySelect/',views.changeManySelect,name="changeManySelect"),
    url(r'^createOrder/',views.createOrder,name="createOrder"),
    url(r'^orderInfo/(.+)',views.orderInfo,name="orderInfo"),
    url(r'^changeOrderStatu',views.changeOrderStatu,name="changeOrderStatu"),
]
