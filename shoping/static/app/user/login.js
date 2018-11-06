

//当点击登录的时候调用
function  formsubmit() {
//    1.空判断,长度判断....


//    将密码用md5处理
    $pass  = $("#password")
    passwd = $pass.val()
    md5passwd = md5(passwd)
//   设置
    $pass.val(md5passwd)

    return true

}


