$(function () {
//    设置默认位隐藏
    $("#type_container").hide()
    $("#allsortrule").hide()

//    给全部类型设置点击事件
    $("#alltypes").click(function () {
    //    显示  子分类
    //    找到 子分类的 div
        $("#type_container").show()
    //    将箭头变成向上
        $("#glyphiconTypes").removeClass().addClass("glyphicon glyphicon-chevron-up")

    //    让 所有排序 隐藏
        $("#allsortrule").hide()
        $("#glyphiconSort").removeClass().addClass("glyphicon glyphicon-chevron-down")

    })


//    点击子分类容器中的的任何一个位置,隐藏该子分类界面
    $("#type_container").click(function () {
        $(this).hide()
        //    将箭头变成向下
        $("#glyphiconTypes").removeClass().addClass("glyphicon glyphicon-chevron-down")
    })

    //点击显示排序规则
    $("#allsort").click(function () {
        $("#allsortrule").show()
    //   改变箭头方向
        $("#glyphiconSort").removeClass().addClass("glyphicon glyphicon-chevron-up")

        $("#type_container").hide()
        //    将箭头变成向下
        $("#glyphiconTypes").removeClass().addClass("glyphicon glyphicon-chevron-down")


    })

    $("#allsortrule").click(function () {
        $(this).hide()
        $("#glyphiconSort").removeClass().addClass("glyphicon glyphicon-chevron-down")
    })



//    点击 + 按钮,将商品加入到购物车

    $(".addToCart").click(function () {

        //获得goodsid (给该button动态添加了 goodsid属性)
        goodsid = $(this).attr("goodsid")

        addUrl = "/axf/addToCart";

        $this = $(this)


    //    ajax请求
        $.getJSON(addUrl,{"goodsid":goodsid},function (data) {
            if(data["code"] == 302){//需要重定向登录
               //打开登录页面
                window.open("/axf/login",target="_self")
            }else if(data["code"] == 200){
                // alert(data["num"])
            //    修改数量

                $this.prev("span").html(data["num"])
            }
        })
    })

//    点击 - 按钮,将商品的购物车数量减去一个
    $(".subToCart").click(function () {
         //获得goodsid (给该button动态添加了 goodsid属性)
        goodsid = $(this).attr("goodsid")

        addUrl = "/axf/subToCart";

        $this = $(this)

        //    ajax请求
        $.getJSON(addUrl,{"goodsid":goodsid},function (data) {
            if(data["code"] == 302){//需要重定向登录
               //打开登录页面
                window.open("/axf/login",target="_self")
            }else if(data["code"] == 200){
                // alert(data["num"])
            //    修改数量
                $this.next("span").html(data["num"])
            }
        })
    })



})







