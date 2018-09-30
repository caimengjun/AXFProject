// 标记密码是否合法
var flag1 = false
var flag2 = false


$(function () {
    // 验证用户名是否已经存在
    $("#username").change(function () {
        //获得用户输入的用户名
        usernameval = $(this).val()
        // 异步请求服务器
        //callback:回调函数,请求成功的时候调用,携带服务器返回的数据
        $.getJSON('/axf/checkUserUnique',{"username":usernameval},function (data) {
            if (data["code"] == 800){
                $("#error_user").html(data["msg"]).css("color","#ff0000")
                flag2 = false
            }else if (data["code"] == 801){
                $("#error_user").html(data["msg"]).css("color","#00ff00")
                flag2 = true

            }

        })
    })

    // 验证设置的密码是否合法
    // 当确认密码框失去焦点,且内容发生改变的时候校验 change
    // password1 设置密码框 password2 确认密码框
    $("#password2").change(function () {
        // alert("xxxx")
        // 1.密码长度至少6位
        // 2.两次输入的密码必须一致
        // 3.输入的密码必须符合规范

        // 获得用户输入的内容
        password1val = $("#password1").val()
        password2val = $("#password2").val()

        if((password1val.length < 6) || (password2val.length<6)){
            // 密码小于6位
            // 提示
            $("#error_info").html("密码至少6位").css("color","rgb(255,0,0)")
            return
        }

        if (password2val != password1val){
            $("#error_info").html("两次输入的密码不一致").css("color","rgb(255,0,0)")
            return
        }

        $("#error_info").html("设置的密码可用").css("color","#00ff00")
        flag1 = true


    })

})
//    from 中 onsubmit属性调用的方法
//    当用户提交form的是很好，会自动调用onsubmit，表示是否可以提交
//    onsubmit True可以提交
function submitCheck() {
    //
    if (!flag2){ // 不合法
        alert("输入的用户名不合法");
        return false
    }

    if (!flag1){ // 不合法
        alert("输入的密码不合法");
        return false
    }

    passwd2 = $("#password2").val();

    res = md5(passwd2);

    // alert(res)
    // console.log(res)

    $("#password1").val(res)

    return true
}



























