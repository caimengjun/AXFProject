from django.db import models

# Create your models here.




# 设计基础数据父类,用来被继承
class  HomeModel(models.Model):
    # 数据的图片地址
    img = models.CharField(max_length=200)
    # 图片的描述名
    name = models.CharField(max_length=100)

    trackid = models.CharField(max_length=50)

#     非关联
    class Meta:
        abstract= True



#设置轮播图数据表
#

# insert into axf_wheel(img,name,trackid) values
# ("http://img01.bqstatic.com//upload/activity/2017031716035274.jpg@90Q.jpg","酸奶女王","21870"),("http://img01.bqstatic.com//upload/activity/2017031710450787.jpg@90Q.jpg","优选圣女果","21869"),("http://img01.bqstatic.com//upload/activity/2017030714522982.jpg@90Q.jpg","伊利酸奶大放价","21862"),("http://img01.bqstatic.com//upload/activity/2017032116081698.jpg@90Q.jpg","鲜货直供－窝夫小子","21770"),("http://img01.bqstatic.com//upload/activity/2017032117283348.jpg@90Q.jpg","鲜货直供－狼博森食品","21874");
class  wheelModel(HomeModel):
      # 轮播图图片地址
      # img = models.CharField(max_length=200)
      # # 轮播图名称描述
      # name = models.CharField(max_length=100)
      #
      # trackid = models.CharField(max_length=50)

#     自定义数据表表明
      class Meta:
          db_table = "axf_wheel"


# insert into axf_nav(img,name,trackid)
# values("http://img01.bqstatic.com//upload/activity/2017032016495169.png","每日必抢","21851"),("http://img01.bqstatic.com//upload/activity/2016121920130294.png","每日签到","21753"),("http://img01.bqstatic.com//upload/activity/2017010517013925.png","鲜货直供","21749"),("http://img01.bqstatic.com//upload/activity/2017031518404137.png","鲜蜂力荐","21854");
# 设计顶部导航nav数据模型
class NavModel(HomeModel):

    class Meta:
        db_table = "axf_nav"



#设计必买数据模型
# insert into axf_mustbuy(img,name,trackid) values("http://img01.bqstatic.com//upload/activity/2017031715194326.jpg@90Q.jpg","酸奶女王","21870"),("http://img01.bqstatic.com//upload/activity/cms_118826_1489742316.jpg@90Q","鲜果女王","21861"),("http://img01.bqstatic.com//upload/activity/2017031011044918.jpg@90Q.jpg","麻辣女王","21866"),("http://img01.bqstatic.com//upload/activity/2017022318314545.jpg@90Q.jpg","鲜货直供－果析","21858");
class Mustbuy(HomeModel):
    class Meta:
        db_table = "axf_mustbuy"


# 设计shop 商店数据模型
# insert into axf_shop(img,name,trackid) values("http://img01.bqstatic.com//upload/activity/2016121616565087.png@90Q.png","闪送超市","1464"),("http://img01.bqstatic.com//upload/activity/2017031018405396.png@90Q.png","热销榜","104749"),("http://img01.bqstatic.com//upload/activity/2017031018403438.png@90Q.png","新品尝鲜","104747"),("http://img01.bqstatic.com//upload/activity/2016121618424334.png@90Q.png","牛奶面包","103536"),("http://img01.bqstatic.com//upload/activity/2016121617150246.png@90Q.png","饮料酒水","103549"),("http://img01.bqstatic.com//upload/activity/201612161714501.png@90Q.png","优选水果","103532"),("http://img01.bqstatic.com//upload/activity/2016121618550639.png@90Q.png","更多","100001"),("http://img01.bqstatic.com//upload/activity/2017031318520359.jpg@90Q.jpg","鲜蜂力荐","21854"),("http://img01.bqstatic.com//upload/activity/2016121618233839.png@90Q.png","卤味-鸭货不能停","21742"),("http://img01.bqstatic.com//upload/activity/2016121618232773.png@90Q.png","零食轰趴","21142"),("http://img01.bqstatic.com//upload/activity/2016121618235123.png@90Q.png","整箱购","20581");
class ShopModel(HomeModel):
    class Meta:
        db_table = "axf_shop"



# 设计 mianshow 表
# insert into axf_mainshow(trackid,name,img,categoryid,brandname,img1,childcid1,productid1,longname1,price1,marketprice1,img2,childcid2,productid2,longname2,price2,marketprice2,img3,childcid3,productid3,longname3,price3,marketprice3)
# values("21782","优选水果","http://img01.bqstatic.com//upload/activity/2017031018205492.jpg@90Q.jpg","103532","爱鲜蜂",
# "http://img01.bqstatic.com/upload/goods/201/701/1916/20170119164159_996462.jpg@200w_200h_90Q","103533","118824","爱鲜蜂·特小凤西瓜1.5-2.5kg/粒","25.80","25.8",
# "http://img01.bqstatic.com/upload/goods/201/611/1617/20161116173544_219028.jpg@200w_200h_90Q","103534","116950","蜂觅·越南直采红心火龙果350-450g/盒","15.3","15.8","http://img01.bqstatic.com/upload/goods/201/701/1916/20170119164119_550363.jpg@200w_200h_90Q","103533","118826","爱鲜蜂·海南千禧果400-450g/盒","9.9","13.8");
class MainshowModel(models.Model):
    # trackid, name, img, categoryid, brandname,
    # img1, childcid1, productid1, longname1, price1, marketprice1,
    # img2, childcid2, productid2, longname2, price2, marketprice2,
    # img3, childcid3, productid3, longname3, price3, marketprice3
    # 数据的图片地址
    img = models.CharField(max_length=200)
    # 图片的描述名
    name = models.CharField(max_length=100)

    trackid = models.CharField(max_length=50)

    categoryid = models.CharField(max_length=50)

    brandname = models.CharField(max_length=50)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=50)
    productid1 = models.CharField(max_length=50)
    longname1 = models.CharField(max_length=200)
    price1 = models.CharField(max_length=50)
    marketprice1 = models.CharField(max_length=50)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=50)
    productid2 = models.CharField(max_length=50)
    longname2 = models.CharField(max_length=200)
    price2 = models.CharField(max_length=50)
    marketprice2 = models.CharField(max_length=50)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=50)
    productid3 = models.CharField(max_length=50)
    longname3 = models.CharField(max_length=200)
    price3 = models.CharField(max_length=50)
    marketprice3 = models.CharField(max_length=50)


    class Meta:
        db_table="axf_mainshow"





# 设计商品分类模型
# 分类名称,商品类型id, 子分类名,
# insert into axf_foodtypes(typeid,typename,childtypenames,typesort)
# values("104749","热销榜","全部分类:0",1),("104747","新品尝鲜","全部分类:0",2),("103532","优选水果","全部分类:0#进口水果:103534#国产水果:103533",3),("103581","卤味熟食","全部分类:0",4),("103536","牛奶面包","全部分类:0#酸奶乳酸菌:103537#牛奶豆浆:103538#面包蛋糕:103540",5),("103549","饮料酒水","全部分类:0#饮用水:103550#茶饮/咖啡:103554#功能饮料:103553#酒类:103555#果汁饮料:103551#碳酸饮料:103552#整箱购:104503#植物蛋白:104489#进口饮料:103556",6),("103541","休闲零食","全部分类:0#进口零食:103547#饼干糕点:103544#膨化食品:103543#坚果炒货:103542#肉干蜜饯:103546#糖果巧克力:103545",7),("103557","方便速食","全部分类:0#方便面:103558#火腿肠卤蛋:103559#速冻面点:103562#下饭小菜:103560#罐头食品:103561#冲调饮品:103563",8),("103569","粮油调味","全部分类:0#杂粮米面油:103570#厨房调味:103571#调味酱:103572",9),("103575","生活用品","全部分类:0#个人护理:103576#纸品:103578#日常用品:103580#家居清洁:103577",10),("104958","冰激凌","全部分类:0",11);
class  foodtypeModel(models.Model):
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


# 用户 表 (注册/登录的表)

class UserModel(models.Model):
#   id,  用户名  32位  唯一, 密码  256位  md5加密  不能为空,邮箱  64位  唯一,手机号, 性别..., 头像 图片  imageField
    u_name = models.CharField(max_length=32,unique=True)
    u_passwd = models.CharField(max_length=32,null=False)
    u_mail = models.CharField(max_length=64,unique=True)
    # ....
    u_sex = models.BooleanField(default=1)
#   头像
    u_img = models.ImageField(upload_to="img")

    class Meta:
        db_table = "axf_user"



# 购物车
# 设计数据库表
#     1.商品id(外建)---关联goods商品表
#     2.商品的数量 ,默认有一个
#     3.是否选中(是否要买)
#     4.用户id(外建)-----关联user用户表
#    商品 ---- 多个用户买
#    用户----多种商品
#     多对多关系---第三张表


class CartModel(models.Model):
    c_goods = models.ForeignKey(Goods)
    c_num = models.IntegerField(default=1)
    c_isselect = models.BooleanField(default=1)
    c_user = models.ForeignKey(UserModel)

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

# 订单表
class OrderModel(models.Model):
    o_number = models.CharField(max_length=128)
    o_user = models.ForeignKey(UserModel)
    o_status = models.IntegerField(default=0)
    o_create_time = models.DateField(auto_now=True)

    class Meta:
        db_table = "axf_order"
# 订单-商品关系表
class OrderAndGoods(models.Model):
    # 订单号
    o_number = models.ForeignKey(OrderModel)
    o_goods  = models.ForeignKey(Goods)
    # 购买数量
    o_count = models.IntegerField(default=1)

    class Meta:
        db_table = "axf_orderandgoods"





























































