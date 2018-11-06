$(function () {
    //    点击 + 按钮,将购物车中商品数量加1

    $(".addCart").click(function () {
        $this = $(this)
        cartid = $this.parents("li").attr("cartid")
        // alert(cartid)
        addUrl = "/axf/addCart";


        //    ajax请求
        $.getJSON(addUrl, {"cartid": cartid}, function (data) {
            if (data["code"] == 200) {
                // alert(data["num"])
                //    修改数量
                $this.prev("span").html(data["num"])
            }
        })
    })


    //    点击 + 按钮,将购物车中商品数量加1

    $(".subCart").click(function () {
        $this = $(this)

        cartid = $this.parents("li").attr("cartid")
        // alert(cartid)

        addUrl = "/axf/subCart";


        //    ajax请求
        $.getJSON(addUrl, {"cartid": cartid}, function (data) {
            if (data["code"] == 200) {
                // alert(data["num"])
                //    修改数量
                $this.next("span").html(data["num"])
            }
            else if (data["code"] == 300) { //移除该整个商品记录
                $this.parents("li").remove()

            }
        })
    })


    //勾选按钮的点击事件
    $(".selectButton").click(function () {
        $this = $(this)
        cartid = $this.parents("li").attr("cartid")

        urlPath = "/axf/chanageSelect"
        $.getJSON(urlPath, {"cartid": cartid}, function (data) {
            if (data["code"] == 200) {//修改状态成功
                // alert(data["isselect"])
                if (data["isselect"]) { //选中
                    $this.html("<span>√</span>")
                    $this.attr("isselect", "True")

                } else {  //不选中
                    $this.html("<span></span>")
                    $this.attr("isselect", "False")
                }

                //   是否全选
                if (data["isAllSelect"]) {
                    $("#allSelectButton").html("<span>√</span>")
                } else {
                    $("#allSelectButton").html("<span></span>")
                }

            }
        })
    })


    //给全选按钮设置点击事件
    $("#allSelectButton").click(function () {
        /*
        * 1.加上勾  只要有一个商品没有被选中, 点击全选按钮, 全选按钮应该变成  选中 按钮, 所有的商品应该变成选中状态
        *
        * 2.去掉勾   当所有商品都被选中的时候,点击全选按钮,全选按钮应该变成  未选中  状态,所有的商品应该变成未选中状态
        * */


        // 获取到所有商品的选中状态---解决: 前端,服务器
        //   未选中的
        var noSelectList = [];
        //所有选中的
        var selectList = [];

        $(".selectButton").each(function () { //遍历每一个selectbutton
            //获得选中状态
            isselect = $(this).attr("isselect")
            //获得当前的cartid
            cartid = $(this).parents("li").attr("cartid")
            console.log(isselect)
            if (String(isselect) == "True") {//选中  python中 True,False    js中 false,true
                selectList.push(cartid)
            } else {
                noSelectList.push(cartid)
            }
        })
        //     测试:

        console.log(noSelectList)
        console.log(selectList)

        if (noSelectList.length == 0 && selectList.length >= 1) {//全部选中---条件2---全选按钮应该变成  未选中  状态,所有的商品应该变成  未选中  状态
            urlPath = "/axf/changeManySelect"
            console.log(selectList)
            $.getJSON(urlPath, {"cartidList": selectList.join("#"), "flag": 2}, function (data) {
                if (data["code"] == 200) {//状态修改成功
                    //    将所有的商品变为选中效果
                    $(".selectButton").each(function () {
                        $(this).html("<span></span>")
                        $(this).attr("isselect", "False")
                    })
                    $("#allSelectButton").html("<span></span>")
                }
            })

        } else { //存在没有被选中的  条件1 ---- 选按钮应该变成  选中 按钮, 所有的商品应该变成选中状态

            urlPath = "/axf/changeManySelect"
            //将未选中的变成选中的
            console.log(noSelectList)
            $.getJSON(urlPath, {"cartidList": noSelectList.join("#"), "flag": 1}, function (data) {
                if (data["code"] == 200) {//状态修改成功
                    //    将所有的商品变为选中效果
                    $(".selectButton").each(function () {
                        $(this).html("<span>√</span>")
                        $(this).attr("isselect", "True")
                    })
                    $("#allSelectButton").html("<span>√</span>")
                }
            })


        }
    })


//  点击选好了按钮,生成一个订单
    $("#greate_order").click(function () {
        //    获取所有的选中的 cartid 购物车记录
        var selectList = [];
        $(".selectButton").each(function () {
            isselect = $(this).attr("isselect")
            cartid = $(this).parents("li").attr("cartid")
            if (String(isselect) == "True") {//选中的
                selectList.push(cartid)
            }
        })

        if (selectList.length == 0) {//没有选中
            alert("没选中任何商品")
        } else {
            // console.log(selectList)
            // 发送给服务器,让服务器生成订单
            urlPath = "/axf/createOrder"
            $.getJSON(urlPath, {"selectList": selectList.join("#")}, function (data) {
                if(data["code"] == 200){
                    orderNumber  = data["orderNumber"]

                //    订单创建成功--调到订单页面
                    window.open("/axf/orderInfo/" + orderNumber ,target="_self")

                }
            })
        }


    })

})



