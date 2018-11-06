//当页面加载完的时候执行

$(function () {
//轮播图
    wheelJs()
//  必买商品轮播图驱动
    mustbuyJs()

})

//顶部轮播图驱动
function wheelJs() {
    var mySwiper = new Swiper ('#topSwiper', {
    loop: true,
     // autoplay:true,  //是否自动滚动
        // speed:3000,  //速度,即间隔多长时间自动切换


    // 如果需要分页器
    pagination: '.swiper-pagination',

  })
}

//必买商品轮播图驱动
function mustbuyJs() {
     var mySwiper = new Swiper ('#swiperMenu', {
     loop: true,  //时候轮回

      slidesPerView: 3,  //显示多少个图片  默认是一张
      spaceBetween: 8,   //间隔空间
         // autoplay:true,  //是否自动滚动
        // speed:3000,  //速度,即间隔多长时间自动切换
  })
    
}

















