import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
#主页
from django.urls import reverse

from app.models import Wheel, Nav, Mustbuy, shop, Mainshow, FoodType, Goods, UserModel, CartModel, OrderModel, \
    DrderAndGoods


def home(request):
    #顶部轮播图的所有数据
    wheels = Wheel.objects.all()

    #查询nav的所有数据
    navs = Nav.objects.all()

    #必买轮播图
    mustbuys = Mustbuy.objects.all()

    #推荐商品
    shops = shop.objects.all()
    shops1 = shops[0]
    shops2_3 = shops[1:3]
    shops4_7 = shops[3:7]
    shops8_ = shops[7:]
    mainShows = Mainshow.objects.all()


    data = {
        "title":"主页",
        "wheels":wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shops1':shops1,
        'shops2_3':shops2_3,
        'shops4_7': shops4_7,
        'shops8_':shops8_,
        'mainShows':mainShows,
    }


    return render(request, 'home/home.html',context=data)
#闪购
def market(request):
    # foodtypes = FoodType.objects.all()
    # goods = Goods.objects.all()
    #
    #
    # data = {
    #     "title":"闪购",
    #     'foodtypes':foodtypes,
    #     'goods':goods,
    # }

    # return render(request, 'market/market.html',context=data)
    return redirect(reverse('axf:marketWithParm',args = (104749,0,0)))
#typeid:商品分类id
#childid:子分类的id
def marketWithParm(request,typeid,childid,sortType):
    foodtypes = FoodType.objects.all()
    # 根据商品类型查询数据

    if str(childid) == "0":
        goods = Goods.objects.filter(categoryid=typeid)
    #再次根据子分类id进行数据帅选
    else:
        goods = Goods.objects.filter(categoryid=typeid).filter(childcid=childid)

    #根据排序类型在结果集上排序
    if int(sortType) == 0:
        pass
    elif int(sortType) ==1:
        goods = goods.order_by("-productnum")
    elif int(sortType) == 2:
        goods = goods.order_by("price")
    elif int(sortType)  ==3:
        goods = goods.order_by("-price")


    #根据类型查询出所有子分类信息
    foodtype = FoodType.objects.filter(typeid=typeid).first()

    childtypenames = foodtype.childtypenames.split("#")
    allChild = []
    for child in childtypenames:
        allChild.append(child.split(":"))
    print(allChild)
    userid = request.session.get("user_id")
    if userid:
        user = UserModel.objects.filter(pk=userid)
        carts = CartModel.objects.filter(c_user=user)

    data = {
        "title": "闪购",
        'foodtypes': foodtypes,
        'goods': goods,
        'typeid':str(typeid),
        'allChild':allChild,
        'childid':int(childid),
        'carts':carts,
    }
    #获得当前用户信息



    return render(request, 'market/market.html', context=data)




# 购物车
def cart(request):

    userid = request.session.get("user_id")
    if userid:
        user = UserModel.objects.filter(pk=userid).first()
    else:
        return redirect(reverse('axf:login'))

    # 根据用户查询该用户所有的cart记录
    carts = CartModel.objects.filter(c_user=user)

    isAllSelect = True
    for cart in carts:
        #只要cart中有一条记录没被选中,则全选一定是false
        if not cart.c_isselect:
            isAllSelect = False
            break

    countAndPrice = totalCountAndPrice(user)


    data = {
        "title": "购物车",
        "carts": carts,
        'isAllSelect':isAllSelect,
        'totalCount':countAndPrice.get("totalCount"),
        'totalPrice':countAndPrice.get("totalPrice"),

    }
    return render(request, "cart/cart.html",context=data)

#我的
def mine(request):
    #获得session的值
    userid = request.session.get("user_id")
    data ={}
    data["title"] ="我的"
    if userid:
        #获取user
        user = UserModel.objects.filter(pk = userid).first()
        data["user"] = user
        data["imgPath"] = '/static/upload/' + user.u_img.url
        #获得各个状态的订单数量
        orders = OrderModel.objects.filter(o_user = user)
        noPayCount = orders.filter(o_status=1).count()
        noCollection = orders.filter(o_status=2).count()
        noEvaluateCount = orders.filter(o_status=3).count()
        refundCount = orders.filter(o_status=4).count()
        data["noPayCount"] =noPayCount
        data["noCollection"] = noCollection
        data["noEvaluateCount"] = noEvaluateCount
        data["refundCount"] = refundCount



    else:
        data["user"] = None



    return render(request, 'mine/mine.html',context=data)

def register(request):
    if request.method =="GET":
        return render(request, "user/register.html")

    elif request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        img = request.FILES.get("img")

        # print(password)

        user = UserModel()
        user.u_name = username
        user.u_password = password
        user.u_email = email
        user.u_img = img

        user.save()

        return redirect(reverse('axf:login'))
#验证用户名的唯一性
def checkUserUnique(request):
    username = request.GET.get("username")
    #根据用户名去查询数据库
    #有结果---存在
    res =UserModel.objects.filter(u_name = username)
    data = {}
    if res.exists():
        data["code"] = 800
        data["msg"] = "用户名已经存在"
    else:
        data["code"] = 801
        data["msg"] = "用户名不存在,可用"

    return JsonResponse(data)

def login(request):
    if request.method == "GET":
        return render(request,'user/login.html')
    elif request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        res = UserModel.objects.filter(u_name=username)
        if res.exists():
            user = res.first()
            mypassword = user.u_password
            if password == mypassword:

                #保存到session
                request.session["user_id"] = user.id
                #进入到我的页面
                return redirect(reverse('axf:mine'))

        return HttpResponse("用户名或密码错误")

def logout(request):
    #清除session
    request.session.flush()

    return redirect(reverse('axf:login'))

#将商品加入到购物车
def addToCart(request):
    # 1.用户,获得登录的用户信息
    #     1.1.登陆了
        # 1.2.没有登录,跳到登录页面
    userid = request.session.get("user_id")
    data = {}
    if userid:
        user = UserModel.objects.filter(pk = userid).first()
    else:
        #在ajax请求中,不能进行重定向,也不能相应HttpResponse
        #可以在js中重定向
        # return redirect(reverse('axf:login'))
        data['code'] = 304 #需要重定向到登录页
        data['msg'] = "未登录,重新登录"
        return JsonResponse(data)
    #2.商品
    #获得商品的id,并找到对应的商品对象
    goodsid = request.GET.get("goodsid")
    mygoods = Goods.objects.filter(pk=goodsid).first()

    #查询cart记录
    res = CartModel.objects.filter(c_user=user).filter(c_goods=mygoods)
    #3.数量
     # 1.购物车中没有记录,新建一条购物车记录,并且数量为1
    #2.购物车中有记录,在原有的记录上加1
    if res.exists():#有记录
        cart = res.first()
        cart.c_num += 1
        cart.save()

        data['code'] = 200 #操作成功
        data['msg'] = "添加到购物车成功"
        data['num'] = cart.c_num

    else:#没有记录
        cart = CartModel()
        cart.c_user = user
        cart.c_goods = mygoods
        cart.c_num = 1
        cart.c_isselect = True

        data['code'] = 200  # 操作成功
        data['msg'] = "添加到购物车成功"
        data['num'] = 1

        cart.save()
    return JsonResponse(data)





#商品数量减1
def subToCart(request):
    userid = request.session.get("user_id")
    data = {}
    if userid:
        user = UserModel.objects.filter(pk=userid).first()
    else:
        # 在ajax请求中,不能进行重定向,也不能相应HttpResponse
        # 可以在js中重定向
        # return redirect(reverse('axf:login'))
        data['code'] = 304  # 需要重定向到登录页
        data['msg'] = "未登录,重新登录"
        return JsonResponse(data)
    # 2.商品
    # 获得商品的id,并找到对应的商品对象
    goodsid = request.GET.get("goodsid")
    mygoods = Goods.objects.filter(pk=goodsid).first()

    # 查询cart记录
    res = CartModel.objects.filter(c_user=user).filter(c_goods=mygoods)
    # 3.数量
    # 1.cart记录不存在
    # 直接返回0
    # 2.cart记录存在
    #   1.数量等于1
    #   删除记录,并返回1
    #   2.数量大于1,则数量减去1
    if res.exists():
        cart = res.first()
        num = cart.c_num
        if num == 1:
            data['code'] = 200
            data['msg'] = '删除成功'
            data['num'] = 0
        else:
            cart.c_num -=1
            cart.save()
            data['code'] = 200
            data['msg'] = '删除成功'
            data['num'] = cart.c_num
    else:
        data['code'] = 200
        data ['msg'] = '购物车没有该记录'
        data['num'] = 0

    return JsonResponse(data)

def addCartNum(request):
    #获取商品id
    cartid = request.GET.get('cartid')
    cart = CartModel.objects.filter(pk = cartid).first()
    cart.c_num +=1
    cart.save()
    data ={}

    data['code'] = 200
    data['msg'] = "数量加操作成功"
    data['num'] = cart.c_num


    return JsonResponse(data)

def subCartNum(request):
    cartid = request.GET.get('cartid')
    cart = CartModel.objects.filter(pk = cartid).first()
    num = cart.c_num
    data = {}

    if num == 1:#如果数量减为0,删除该条数据
        cart.delete()
        data['code'] = 201
        data['msg'] = "数量加操作成功"
        data['num'] = 0
    elif num >1:
        cart.c_num -=1
        cart.save()
        data['code'] = 200
        data['msg'] = "数量加操作成功"
        data['num'] = cart.c_num

    return JsonResponse(data)


def iscunzai(request):
    userid = request.session.get("user_id")
    data = {}
    if userid:
        carts = CartModel.objects.filter(c_user=userid).all()
    else:
        # 在ajax请求中,不能进行重定向,也不能相应HttpResponse
        # 可以在js中重定向
        # return redirect(reverse('axf:login'))
        data['code'] = 304  # 需要重定向到登录页
        data['msg'] = "未登录,重新登录"
        return JsonResponse(data)
    sum = []
    sum1 = []
    for cart in carts:
        sum.append(str(cart.c_goods_id))
        sum1.append(str(cart.c_num))

    str1 = "#".join(sum)
    str2 = "#".join(sum1)
    print(str1)
    data['code'] = 200
    data['msg'] = "数量加操作成功"
    data['goodid'] = str1
    data['num'] = str2

    return JsonResponse(data)


def changeSelectStatu(request):
    #获取订单号
    cartid = request.GET.get("cartid")
    userid = request.session.get("user_id")
    #获取当前id的整条记录
    cart = CartModel.objects.filter(pk = cartid).first()

    cart.c_isselect = not cart.c_isselect
    cart.save()
    #查询出订单记录
    #修改订单的状态
    data = {}
    CountAndPrice = totalCountAndPrice(userid)
    data['totalCount'] = CountAndPrice.get("totalCount")
    data['totalPrice'] = CountAndPrice.get("totalPrice")

    data['code'] = 200
    data['msg'] = "状态修改成功"
    data['isselect'] = cart.c_isselect

    #判断是否全选, 当有一个没选则不是全选, 必须所有都选中才全选

    if userid:
        carts = CartModel.objects.filter(c_user=userid).all()
    else:
        data['code1'] = 304  # 需要重定向到登录页
        return JsonResponse(data)

    for cart in carts:
        if cart.c_isselect == False:
            data['code1'] = 201
            return JsonResponse(data)

    data["code1"] = 200

    #计算总价格和总数量


    return JsonResponse(data)




#点击全选按钮时修改多条数据的选中状态
def changeManySelectStatu(request):
    selectList = request.GET.get("selectList").split("#")
    print(selectList)
    flag = request.GET.get("flag")
    data={}
    carts = CartModel.objects.filter(id__in= selectList)
    for cart in carts:
        #也可以用not,不用判断flag
        if flag == "1":#全改为false
            cart.c_isselect = False

        elif flag =="0":
            cart.c_isselect = True

        cart.save()

    data['code'] = 200



    return JsonResponse(data)



#定义一个函数用来计算选中的商品数量和总价格
def totalCountAndPrice(user):
    #查询出所有选中是商品
    carts = CartModel.objects.filter(c_user=user).filter(c_isselect=True)

    #选中的商品数量
    totalCount = 0

    #x选中商品的总价格
    totalPrice = 0

    for cart in carts:
        totalCount += cart.c_num
        totalPrice += cart.c_num * cart.c_goods.price

    # return (totalCount,totalPrice)
    return {"totalCount":totalCount,"totalPrice":totalPrice}

#创建一个订单
'''
目的:生成一个订单
1.订单号 --uuid
2.用户--获得user_id,查询出对应的user
3.设置时间(自动)
4.设置状态(待付款 1)
5.保存

创建多个订单商品关系
1.获得所有选中cart记录,遍历记录

创建一个订单关系
订单号--关联上方的订单
商品对象---cart中

'''
def createOrder(request):
    userid = request.session.get("user_id")
    #判断是否登录(没写)

    user = UserModel.objects.filter(pk = userid).first()
    order = OrderModel()
    order.o_num = str(uuid.uuid4())
    order.o_user = user
    order.o_status = 1 #表示待付款

    order.save()

    cartidlist = request.GET.get("selectArray").split("#")

    print(cartidlist)
    carts = CartModel.objects.filter(id__in = cartidlist)
    for cart in carts:
        orderAndGoods = DrderAndGoods()
        orderAndGoods.og_order = order
        orderAndGoods.og_goods = cart.c_goods
        orderAndGoods.og_num = cart.c_num

        orderAndGoods.save()

        cart.delete()
    data = {}
    data['code'] = 200
    #订单号
    data['ordernum'] = order.o_num

    return JsonResponse(data)

#查询订单信息展示出来
def orderInfo(request,orderNum):
    # print(orderNum)

    #查询该订单下所有的商品信息
    order = OrderModel.objects.filter(o_num=orderNum).first()
    orderAndGoods  = DrderAndGoods.objects.filter(og_order=order)
    statu = order.o_status
    if statu == 0:
        orderStatu = "无效"
    elif statu == 1:
        orderStatu ="待付款"
    elif statu == 2:
        orderStatu ="待收货"
    elif statu == 3:
        orderStatu = "待评价"
    elif statu == 4:
        orderStatu = "退款"
    data={
        "title":"订单详情页",
        "orderAndGoods":orderAndGoods,
        'orderNum':orderNum,
        "orderStatu":orderStatu,
    }

    return render(request,"cart/orderinfo.html",context=data)

def changeOrderStatu(request):
    #获取订单号和要改的状态
    status = request.GET.get("status")
    #订单号
    orderNum = request.GET.get(("orderNum"))


    order = OrderModel.objects.filter(o_num =orderNum).first()

    order.o_status = status

    order.save()
    data = {}
    data['code'] = 200

    return JsonResponse(data)