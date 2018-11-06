import uuid

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.

# 主页
from django.urls import reverse

from app.models import wheelModel, NavModel, Mustbuy, ShopModel, MainshowModel, foodtypeModel, Goods, UserModel, \
    CartModel, OrderModel, OrderAndGoods
from axf1805 import settings


def home(request):
    # 获得轮播图数据
    wheeldatas = wheelModel.objects.all()

    # 获取nav导航数据
    navDatas = NavModel.objects.all()

    # 获取必买的数据
    mustbuys = Mustbuy.objects.all()

    # 获取shop商店数据
    shops = ShopModel.objects.all()

    # 将shops数据,拆分开来
    shops0 = shops[0]
    shops1_2 = shops[1:3]
    shops3_6 = shops[3:7]
    shops7_10 = shops[7:]


    # 获取mainshow的所有数据
    mainshows = MainshowModel.objects.all()




    # 设置数据
    data = {
        "wheeldatas":wheeldatas,
        "navDatas":navDatas,
        "mustbuys":mustbuys,
        "shop0":shops0,
        "shops1_2":shops1_2,
        "shops3_6":shops3_6,
        "shops7_10":shops7_10,
        "mainshows":mainshows,
    }



    return  render(request, "home/home.html",context=data)


#闪购页面
def market(request):
    # 获取到所有的商品类型
    # foodtypes = foodtypeModel.objects.all()
    #
    #
    # # 获取到所有的商品
    # goodsall = Goods.objects.all()
    #
    #
    # data = {
    #     "foodtypes":foodtypes,
    #     "goodall":goodsall,
    # }


    # 默认展示热销榜数据
    return  HttpResponseRedirect(reverse("axf:market_param",args=(104749,0,0)))

# typeid是用来商品分类的商品类型id
# childtypeid 是商品子分类id, 可以根据该id筛选出子分类数据
# sortType 是排序类型
def marketWithParam(request,typeid,childtypeid,sortType):
    # 获取到所有的商品类型
    foodtypes = foodtypeModel.objects.all()


    # typeid是foodtype中主分类的类型id
    # 获取到所有的商品
    if childtypeid == "0": #全部分类
      goodsall = Goods.objects.filter(categoryid=typeid)
    else:
      goodsall = Goods.objects.filter(categoryid=typeid).filter(childcid=childtypeid)

    # print(len(goodsall))

    # 在原有的查询结果上排序
    sortType = str(sortType)
    if sortType == "0":   #综合排序
        pass
    elif sortType == "1":  #销量排序
       goodsall = goodsall.order_by("productnum")
    elif sortType == "2":    #价格降序
        goodsall =goodsall.order_by("-price")
    elif sortType == "3":   #价格升序
        goodsall = goodsall.order_by("price")


    # 根据 typeid 来获取所有的子分类信息
    foodtype = foodtypeModel.objects.filter(typeid=typeid).first()
    # foodtypes = foodtypeModel()
    # 全部分类: 0  # 饮用水:103550#茶饮/咖啡:103554#功能饮料:103553#酒类:103555#果汁饮料:103551#碳酸饮料:103552#整箱购:104503#植物蛋白:104489#进口饮料:103556
    # 将子分类拆分开来
    childtypenames = foodtype.childtypenames.split("#")

    childNameAndIds = []

    # print(childtypenames)
    for childType in childtypenames:
        # "饮用水: 103550"
       childNameAndId = childType.split(":") # [饮用水,103550]
       childNameAndIds.append(childNameAndId)


    print(childNameAndIds)
    data = {
        "foodtypes": foodtypes,
        "goodall": goodsall,
        "currentType":typeid,
        "childNameAndIds":childNameAndIds,
        "currentChildid":childtypeid,
    }

    return render(request, "market/market.html", context=data)


# 购物车界面
def cart(request):
    #必须先登录
    # 判断是否登录
    userid = request.session.get("user_id")
    # print(userid)
    if userid:  # 登录
        user = UserModel.objects.filter(pk=userid).first()
        # 根据用户查询出该用户所有的购物车记录]
        carts = CartModel.objects.filter(c_user=user)

        totalNumberPrice  = totalNumberAndPrice(user)


        # 订单是否全部选中
        isAllSelect = True
        for cart in carts:
            # cart = CartModel()
            if not cart.c_isselect: #没有选中
                isAllSelect = False

        data = {
            "carts":carts,
            "is_allselect":isAllSelect,
            "selectCount":totalNumberPrice.get("selectCount"),
            "totalPrice":totalNumberPrice.get("totalPrice"),
        }

        return render(request, "cart/cart.html",context=data)
    return  redirect(reverse("axf:login"))

#我的界面
def mine(request):
    # 判断是否登录
    userid = request.session.get("user_id")
    print(userid)
    if userid:#登录
        user = UserModel.objects.filter(pk=userid).first()
        # user = UserModel()
        # 获得图片的static地址
        # print(user.u_img.path) #绝对路径
        # print(user.u_img.url)  相对路径
        # /static/upload  +
        imgUrl = "/static/upload/"  + user.u_img.url
        print(imgUrl)

        #     获得各种状态的订单数量
        # 查出该用户下的所有订单
        objects = user.ordermodel_set
        nopay = objects.filter(o_status=1).count()  #待付款
        noCollect = objects.filter(o_status=2).count() #待收货
        noEvaluate = objects.filter(o_status=3).count() #待评价
        returnGoods = objects.filter(o_status=4).count() #退款/退货
        # 注意如果没有获取到值,count为 0

        # print(nopay)
        # print(noCollect)
        # print(noEvaluate)
        # print(returnGoods)

        data ={
            "user":user,
            "imgUrl":imgUrl,
            "nopay":nopay,
            "noCollect":noCollect,
            "noEvaluate":noEvaluate,
            "returnGoods":returnGoods,
        }
        return  render(request, "mine/mine.html",context=data)

    else: #没有登录
        return  render(request, "mine/mine.html",context={"user":None})


# 注册界面
def register(request):
    method = request.method
    if method == "GET":#展示注册界面
        return render(request, "user/user_register.html")

    elif method  == "POST":#处理注册请求
        #  获取数据
        postParam = request.POST
        username = postParam.get("username")
        password = postParam.get("password")
        email = postParam.get("email")
        imgFile = request.FILES.get("imgFile")

        # 保存到数据库中
        userModel = UserModel()
        userModel.u_name = username
        # userModel.u_passwd = pass
        # print(password)
        userModel.u_passwd = password
        userModel.u_mail = email
        userModel.u_img = imgFile

        userModel.save()

        # 重定向到登录界面
        # return  HttpResponse("注册成功")
        return  redirect(reverse("axf:login"))

# 检查用户名唯一性
def checkUser(request):
    # 获取到客户端传入的用户名
    username = request.GET.get("username")
    #检查数据库是否拥有该用户名
    resQuery = UserModel.objects.filter(u_name=username)
    data = {}
    if resQuery.exists():#存在
        data["code"] = 901  #表示已经存在
        data["msg"] = "该用户已经存在"

    else:
       data["code"] = 200  #表示用户名可用
       data["msg"] = "用户名可用"

    # 返回json数据
    return  JsonResponse(data)


# 登录
def login(request):
    if request.method == "GET":
        return  render(request,"user/user_login.html")
    if request.method == "POST":
        # 获取账号密码
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print(username)
        # print(password)

        resQu = UserModel.objects.filter(u_name=username)
        if resQu.exists():#用户存在
            user = resQu.first()
            # user = UserModel()
            # print(user.u_passwd)
            # 验证密码
            if password == user.u_passwd:#验证密码
        #         登录成功
        #         保留session,用来用户认证
        #         跳到mine我的页面,展示个人信息
                request.session["user_id"] = user.id

                return  redirect(reverse("axf:mine"))
        # 登录失败
        return  redirect(reverse("axf:login"))


# 退出账号
def loginOut(request):
    # 清楚账号信息
    request.session.flush()

    return  redirect(reverse("axf:login"))


# 将数据添加到购物车
def addToCart(request):
    # 购物车数据需要: 商品的id, 商品的数量, 商品的选中状态(默认选中),用户

    # 获得用户信息---session
    user_id = request.session.get("user_id")
    data = {}

    if user_id:
        user = UserModel.objects.filter(pk=user_id).first()

    else: #未登录,需要登录

        # 注意:在ajax中不能使用重定向
        # return redirect(reverse('axf:login'))
    #   告诉前段需要重新登录
        data["code"] = 302 #需要重定向
        data["msg"] = "未登录,需要重新登录"
        return  JsonResponse(data)



    # 获得商品id
    goodsid = request.GET.get("goodsid")
    goods = Goods.objects.filter(pk=goodsid).first()

    # 商品数量
    # 如果数据库中没有该数据,设置默认值为1
    # 如果数据库中有该数据---查询出来,则在原有数据量上加1

    # 根据用户来查数据,然后再过滤该商品的购物车数据
    cartRes = CartModel.objects.filter(c_user=user).filter(c_goods=goods)

    if cartRes.exists(): # 找到了购物车记录
        cart = cartRes.first()
        # cart = CartModel()
        cart.c_num +=1
        cart.save()
        data["code"] = 200 #添加成功
        data["msg"] = "加入到购物车成功"
        data['num'] = cart.c_num
    else:#没有找到
    #     创建一个新的购物车记录
        cart = CartModel()
        cart.c_user = user
        cart.c_goods = goods
        cart.c_num = 1
        cart.c_isselect = True
        cart.save()
        data['code'] = 200
        data["msg"] = "加入到购物车成功"
        data['num'] = 1
    return  JsonResponse(data)

# 将购物车中商品数量 减一个
def subToCart(request):
    # 购物车数据需要: 商品的id, 商品的数量, 商品的选中状态(默认选中),用户

    # 获得用户信息---session
    user_id = request.session.get("user_id")
    data = {}

    if user_id:
        user = UserModel.objects.filter(pk=user_id).first()

    else:  # 未登录,需要登录
        print("--------------------")
        # 注意:在ajax中不能使用重定向
        # return redirect(reverse('axf:login'))
        #   告诉前段需要重新登录
        data["code"] = 302  # 需要重定向
        data["msg"] = "未登录,需要重新登录"
        return JsonResponse(data)

    # 获得商品id
    goodsid = request.GET.get("goodsid")
    goods = Goods.objects.filter(pk=goodsid).first()

    # 商品数量
    # 如果数据库中没有该数据,设置默认值为1
    # 如果数据库中有该数据---查询出来,则在原有数据量上加1

    # 根据用户来查数据,然后再过滤该商品的购物车数据
    cartRes = CartModel.objects.filter(c_user=user).filter(c_goods=goods)
    if cartRes.exists():#存在购物车记录
        cart = cartRes.first()
        # cart = CartModel()
        if cart.c_num == 1:#删除该记录
            cart.delete()
            data["code"]  = 200
            data["msg"] = "操作成功"
            data["num"] = 0
        else:#大于1
            cart.c_num -=1
            cart.save()
            data["code"] = 200
            data["msg"] = "操作成功"
            data["num"] = cart.c_num
    else: #不存在
        data["code"] = 200
        data["msg"] = "操作成功"
        data["num"] = 0

    return  JsonResponse(data)



# 修改购物车中商品的数量 加操作
def addCart(request):
#     获取cartid
    cartid = request.GET.get("cartid")
    print(cartid + "*****************")
    cart = CartModel.objects.filter(pk=cartid).first()
    # cart = CartModel()
    cart.c_num +=1
    cart.save()
    data = {}
    data["code"] = 200 #添加成功
    data["msg"] = "加入到购物车成功"
    data['num'] = cart.c_num
    return JsonResponse(data)


#
def subCart(request):
    cartid = request.GET.get("cartid")
    cart = CartModel.objects.filter(pk=cartid).first()
    # cart = CartModel()
    data = {}
    if cart.c_num == 1:#删除cart记录
        cart.delete()
        data["code"] = 300  # 商品数量为0,应该一出该cart记录
        data["msg"] = "移除该购物车记录"
        return JsonResponse(data)
    elif cart.c_num > 1:
        cart.c_num -= 1
        cart.save()
        data["code"] = 200  # 添加成功
        data["msg"] = "数量减少成功"
        data['num'] = cart.c_num
        return JsonResponse(data)

# 改变购物车中商品的选中状态
def chanageSelect(request):
#     查询出cart记录,需要cartid
#     获取cartid
    cartid = request.GET.get("cartid")
    cart = CartModel.objects.filter(pk=cartid).first()
    # cart = CartModel()
#     修改选中状态
    cart.c_isselect = not cart.c_isselect
    cart.save()


    # 是否全选
    user_id = request.session.get("user_id")
    user = UserModel.objects.filter(pk=user_id).first()
    # 获得该用户下的所有的购物车数据
    carts = CartModel.objects.filter(c_user=user)

    isAllSelect = True
    for cart1 in carts:
        # cart = CartModel()
        if not cart1.c_isselect:
            isAllSelect = False

    data = {}
    print(cart.c_isselect)
    data = {
        "code":200,
        "msg":"修改状态成功",
        "isselect":cart.c_isselect,
        "isAllSelect":isAllSelect,
    }
    return  JsonResponse(data)


# 改变多条数据的选中状态
def changeManySelect(request):

#     查询出多条cart记录
#     获取多条cartid   id1#id2#
    print(request.GET.get("cartidList"))
    cartidList = request.GET.get("cartidList").split("#")
    flag = request.GET.get("flag")

    data = {}
    print(cartidList)
    for cartid in cartidList:
        cart  =  CartModel.objects.filter(pk=cartid).first()
        # cart = CartModel()
        if flag == "1":
            cart.c_isselect = True
            data["msg"] = "全部变为选中"
        elif flag == "2":
            cart.c_isselect = False
            data["msg"] = "全部变为未选中"

        cart.save()

    data["code"] = 200

    return JsonResponse(data)


# 计算选中的数量及总价
def totalNumberAndPrice(user):

#   获取该用户所有的订单
   cartsSelect = CartModel.objects.filter(c_user=user).filter(c_isselect=True)
#     计算选中数量
   selectCount = 0
   totalPrice = 0
   for cart in cartsSelect:
       goods = cart.c_goods
       totalPrice += goods.price * cart.c_num
       selectCount += cart.c_num

   #  作业: 点击全选按钮, 点击单个商品选中按钮时,选中数量与总价格随之发生变化
   return  {"selectCount":selectCount,"totalPrice":totalPrice}


# 生成一个订单
def createOrder(request):
    user_id = request.session.get("user_id")
    user = UserModel.objects.filter(pk=user_id).first()

#     创建一个订单
    order = OrderModel()
    # 订单号
    order.o_number = str(uuid.uuid4())
    print(order.o_number)
    order.o_user = user #绑定用户
    order.o_status = 1 #未付款状态
    order.save()

#     创建多个订单商品关系
#     获得购物车中选中的商品
    print(request.GET.get("selectList"))
    cartids = request.GET.get("selectList").split("#")
    for cartid in cartids:
        # 获取购物车中选中的cart
        cart = CartModel.objects.filter(pk=cartid).first()
        # cart = CartModel()
        orderAndGoods = OrderAndGoods()
        orderAndGoods.o_number = order #绑定订单
        orderAndGoods.o_goods = cart.c_goods #绑定商品
        orderAndGoods.o_count = cart.c_num  #绑定商品数量
        orderAndGoods.save()

#       删除购物车中对应的记录
        cart.delete()
#   告诉服务器,订单已经创建ok
    data = {}
    data["code"] = 200
    print("xxxxxx")
    # 订单号
    data["orderNumber"] = order.o_number  #订单号

    return  JsonResponse(data)


# 展示当前订单信息
def orderInfo(request,orderNumber):
    # 获取到订单号
    print(orderNumber)
    print("-----")
    # 根据订单号查询出 对应的商品
    order = OrderModel.objects.filter(o_number=orderNumber).first()
    # order = OrderModel()
    # 获取该订单下的所有的商品
    orderAndGoodses  = order.orderandgoods_set.all()

    data = {
        "orderNumber":orderNumber,
        "orderAndGoodses":orderAndGoodses,
    }



    return  render(request,"cart/orderInfo.html",context=data)


# 改变订单状态
def changeOrderStatu(request):
#    获取订单号
    ordernumber = request.GET.get("ordernumber")
    status = request.GET.get("status")


    order = OrderModel.objects.filter(o_number=ordernumber).first()

    # order = OrderModel()
    order.o_status = status
    order.save()
    data = {
        "code":200,
    }
    return  JsonResponse(data)


# 待付款,待收货.....








