$(function () {


    
    
    //    点击 + 按钮,将购物车中商品数量加1

    $(".addCart").click(function () {
        $this = $(this)
        cartid = $this.parents("li").attr("cartid")
        // alert(cartid)
        addUrl = "/axf/addCartNum";


        //    ajax请求
        $.getJSON(addUrl, {"cartid": cartid}, function (data) {
            if (data["code"] == 200) {
                // alert(data["num"])
                //    修改数量
                $this.prev("span").html(data["num"])
            }
        })
    })


    //    点击 - 按钮,将购物车中商品数量-1

    $(".subCart").click(function () {
        $this = $(this)

        cartid = $this.parents("li").attr("cartid")
        // alert(cartid)

        addUrl = "/axf/subCartNum";


        //    ajax请求
        $.getJSON(addUrl, {"cartid": cartid}, function (data) {
            if (data["code"] == 200) {
                // alert(data["num"])
                //    修改数量
                $this.next("span").html(data["num"])
            }
            else if (data["code"] == 201) { //移除该整个商品记录
                $this.parents("li").remove()

            }
        })
    })


    //勾选按钮的点击事件
 $('.selectButton').click(function () {
        let $this = $(this);
        let cartid = $this.parents('li').attr('cartid');

        let urlPath = '/axf/changeSelectStatu';
        let paramData = {'cartid': cartid};


        // 修改服务器中的状态
        $.getJSON(urlPath,paramData,function (data) {
            if(data['code'] == 200 ){//请求成功
                if(data['isselect']){
                    $this.children('span').text('√')
                    //修改状态
                    $this.attr("isselect","True")
                }else{
                    $this.children('span').text('')
                    $this.attr('isselect','False')
                }
                //判断是否全选,当有一个没选则不是全选,必须所有都选中才全选
                if(data['code1'] == 200) {
                    // $this.parents("li").next("li").children('div').children('span').children('span').text("√")
                    $("#allSelectButton").children("span").text("√")
                }
                else if(data['code1'] == 201){
                    $("#allSelectButton").children("span").text("")
                    // $this.parents("li").next("li").children('div').children('span').children('span').text("")
                }
                else if(data['code1'] == 304){
                    window.open("/axf/login", target = "_self")

                }
                $("#total_Count").html("共计:"+data["totalCount"] + "件")
                $("#total_Price").html("总价:"+data["totalPrice"])

            }






        })
        //显示价格和数量


    })


    //给全选按钮设置点击事件
    $("#allSelectButton").click(function () {
        /*
        * 1.加上勾  只要有一个商品没有被选中, 点击全选按钮, 全选按钮应该变成  选中 按钮, 所有的商品应该变成选中状态
        *
        * 2.去掉勾   当所有商品都被选中的时候,点击全选按钮,全选按钮应该变成  未选中  状态,所有的商品应该变成未选中状态
        * */


        // 获取到所有商品的选中状态---解决: 前端,服务器
        // //   未选中的
        var noSelectList = [];
        //所有选中的
        var selectList = [];

        $(".selectButton").each(function () { //遍历每一个selectbutton
            //获得选中状态
            isselect = $(this).attr("isselect")
            //获得当前的cartid
            cartid = $(this).parents("li").attr("cartid")
            if (String(isselect) == "True") {//选中  python中 True,False    js中 false,true
                selectList.push(cartid)
            } else {
                noSelectList.push(cartid)
            }
        })
       console.log(selectList)
        console.log(noSelectList)


        //判断全选
        if (selectList.length >=1 && (noSelectList.length == 0)){
            //点击全选,变为全部不选中
            urlPath = '/axf/changeManySelectStatu'
            dataParam = {"selectList":selectList.join("#"),"flag":"1"}

            $.getJSON(urlPath,dataParam,function (data) {
                if(data['code'] == 200){
                    $(".selectButton").each(function () {
                        $(this).children('span').text('')
                        $(this).attr("isselect","False")
                    })
                    $("#allSelectButton").children('span').text("")
                }
            })
        }else {
            //当前购物车中部分选中
            //,当点击全选按钮的时候,全选按钮的钩要加上,其他所有单个的也要加上
             //点击全选,变为全部不选中
            urlPath = '/axf/changeManySelectStatu'
            dataParam = {"selectList":noSelectList.join("#"),'flag':"0"}

            $.getJSON(urlPath,dataParam,function (data) {
                 if(data['code'] == 200) {
                     $(".selectButton").each(function () {
                         $(this).children('span').text('√')
                         $(this).attr("isselect", "True")
                     })
                     $("#allSelectButton").children('span').text("√")
                 }
                 })
        }

    })
    // 创建一个订单
    $("#create_order_button").click(function () {

        var allSelectArry = []
        //获取选中的商品
        $(".selectButton").each(function () {
            $this = $(this)
            isselect = $this.attr("isselect")
            cartid = $this.parents("li").attr("cartid")
            if(String(isselect) == "True"){
                allSelectArry.push(cartid)
            }
        })

        //判断是否有选中商品
        if (allSelectArry.length ==0){
            alert("没有选中任何商品")
            return
        }

        urlPath = "/axf/createOrder"
        dataParam = {"selectArray":allSelectArry.join("#")}
        $.getJSON(urlPath,dataParam,function (data) {
            if(data['code'] == 200){
                window.open('/axf/orderInfo/'+data['ordernum'],target="_self")

            }
        })
    })

    
    
    
})



