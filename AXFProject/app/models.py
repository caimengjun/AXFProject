
from django.db import models

# Create your models here.

#定义一个父模型
class  Home(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    trackid = models.CharField(max_length=50)

    class Meta:
        abstract = True

#轮播图
class Wheel(Home):
    class Meta:
        db_table ="axf_wheel"

#nva导航
class Nav(Home):
    class Meta:
        db_table = "axf_nav"

#必买
class Mustbuy(Home):
    class Meta:
        db_table = "axf_mustbuy"

class shop(Home):
    class Meta:
        db_table='axf_shop'

class Mainshow(models.Model):
    trackid = models.CharField(max_length=16)
    name = models.CharField(max_length=50)
    img = models.CharField(max_length=200)
    categoryid = models.CharField(max_length=16)
    brandname = models.CharField(max_length=50)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=50)
    productid1 = models.CharField(max_length=50)
    longname1 = models.CharField(max_length=200)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=0)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=50)
    productid2 = models.CharField(max_length=50)
    longname2 = models.CharField(max_length=200)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=0)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=50)
    productid3 = models.CharField(max_length=50)
    longname3 = models.CharField(max_length=200)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table="axf_mainshow"

class  FoodType(models.Model):
    typeid = models.CharField(max_length=50)
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=-1) #排序字段

    class Meta:
        db_table = "axf_foodtypes"

#设计商品模型
# insert into axf_goods(productid,productimg,productname,productlongname,isxf,pmdesc,specifics,price,marketprice,categoryid,childcid,childcidname,dealerid,storenums,productnum)
# values("11951","http://img01.bqstatic.com/upload/goods/000/001/1951/0000011951_63930.jpg@200w_200h_90Q","","乐吧薯片鲜虾味50.0g",0,0,"50g",2.00,2.500000,103541,103543,"膨化食品","4858",200,4);
class Goods(models.Model):
    productid = models.CharField(max_length=100)
    productimg = models.CharField(max_length=200)
    productname =models.CharField(max_length=50)
    productlongname = models.CharField(max_length=200)
    isxf = models.BooleanField(default=0)
    pmdesc = models.IntegerField(default=0)
    specifics = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=0)
    categoryid =  models.CharField(max_length=50)
    childcid = models.CharField(max_length=50)
    childcidname = models.CharField(max_length=100)
    dealerid = models.CharField(max_length=50)
    storenums = models.IntegerField(default=0)
    productnum = models.IntegerField(default=0)

    class Meta:
        db_table = "axf_goods"

#用户模型
#用户名:唯一
#密码:md5处理
#逻辑删除,
class UserModel(models.Model):
    u_name  =  models.CharField(max_length=32,unique=True)
    u_password = models.CharField(max_length=32)
    u_email = models.CharField(max_length=50,unique=True)
    u_sex = models.BooleanField(default=1)
    #逻辑删除
    u_isdelete = models.BooleanField(default=False)
    u_img = models.ImageField(upload_to="img")


    class Meta:
        db_table = "axf_user"

#设计购物车数据模型
# 用户 user --- 关联用户表 ,外键
# 商品 goods ---- 关联商品表,外键
# 商品数量 num
# 是否选中 isselect

#多对多
class CartModel(models.Model):
    c_user = models.ForeignKey(UserModel)
    c_goods = models.ForeignKey(Goods)
    c_num = models.IntegerField(default=1)
    c_isselect = models.BooleanField(default=True)


    class Meta:
        db_table = "axf_cart"

# 订单信息
#    1.订单表
#       1.订单号 ---唯一
#       2.用户名----外键
#       3.商品*** ---- 多个 ---不放在该表
#       4.订单创建的时间
#       5.订单状态
#          0.无效 ---- 0
#          1.待付款 ---  1
#          2.待收货  ---- 2
#          3.待评价   ---- 3
#          4.退款/售后  ---- 4
#
#
#    2.商品 N-- N订单关系表
#       1.订单号 --- 外键 订单表
#       2.商品  --- 外键
#       3.数量
#订单表
class OrderModel(models.Model):
    o_num = models.CharField(max_length=64)
    o_user = models.ForeignKey(UserModel)
    o_time = models.DateTimeField(auto_now_add=True)
    o_status = models.IntegerField(default=0)

    class Meta:
        db_table="axf_order"

#订单商品表
class DrderAndGoods(models.Model):
    og_order = models.ForeignKey(OrderModel)
    og_goods = models.ForeignKey(Goods)
    og_num = models.IntegerField(default=1)

    class Meta:
        db_table="axf_order_goods"