//标记密码是否合法
var flag1 = false;
//标记用户名是否合法
var flag2 = false;

$(function () {
    //校验用户名是否已经存在
    //当用户名输入框失去焦点且输入框中的内容发生改变的是否校验 change事件
    $("#username").change(function () {
    //  请求服务器校验...
        username = $(this).val()

        /*
        // 参数1: url地址
        // 参数2: data 请求参数  key-value
        // 参数3: callback回调函数, 当请求成功之后调用,data是服务器返回的数据
        // */
        $.getJSON("/axf/checkUser",{"username":username},function (data) {
            // data 是json数据  和python中的字典类似,当作字典来用
            //取值  json数据[key]
            $name =  $("#nameError")
            if(data["code"] == 200){
                $name.html("用户名可用!").css("color","rgb(0,255,0)")
                flag2 = true
            }else if (data["code"] == 901) {
                $name.html("用户名已经存在!").css("color","rgb(255,0,0)")
                flag2 = false

            }
        })


    })


    //校验设置的密码是否合法
    $("#password2").change(function () {
        // alert("xxxx")
    //    验证密码的合法性
    //      1.密码的长度
    //       2.两次输入的密码必须一致，
    //      ××3.密码的组成

       passwd1 =  $("#password1").val()
       passwd2 =  $("#password2").val()
       if(passwd1.length <= 6){
           $("#errorMsg").html("密码长度至少6位").css("color","red")
           flag1 = false

           return
       }

       //判断两次密码输入是否一致
       if (passwd1 != passwd2){
             $("#errorMsg").html("两次输入的密码不一致,请重新设置").css("color","red")
           flag1 = false
            return
       }

    //   验证通过
        $("#errorMsg").html("密码合法").css("color","green")
        flag1 = true
    })
})



//表单提交的时候调用-- 用来验证输入的合法性   onsubmit="return formsubmit"
//注意: 提交的时候会根据该函数的返回值决定是(true)否(false)提交给服务器,
function formsubmit() {
    //验证
    if(!flag1){ //密码不合法
        alert("密码不合法,不能提交")
        return false
    }

    // alert($("#nameError").css("color"))
    // if((String($("#nameError").css("color"))) != "rgb(0,255,0)"){
    //     alert("用户名不合法,不能提交")
    //     return false
    // }

    if(!flag2){
        alert("密码不合法,不能提交")
        return false
    }

    password2 = $("#password2").val()
    //将密码进行md5处理后再提交
    //进行md5处理,会获得md5处理后的结果
    md5Res = md5(password2)
    // alert(md5Res)

    //将密码框中的内容换成MD5结果
    $("#password2").val(md5Res)

    return true; //提交
}




























