$(function () {

    $("#payButton").click(function () {
    //    支付: 支付宝,微信,网银---- 第三方: ping ++
    //    假设已经成功付款

        $this = $(this)
    //    改变订单状态
        urlPath = "/axf/changeOrderStatu"
        ordernumber = $this.attr("orderNumber")
        $.getJSON(urlPath,{"ordernumber":ordernumber,"status":2},function (data) {
            if(data["code"] == 200){//请求成功
                window.open("/axf/mine",target="_self")
            }

        })
    })


})



