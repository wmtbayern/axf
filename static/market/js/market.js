$(function () {
    /* jquery.cookie 用法
     # 设置
     $.cookie(key, value, arg)

     # 获取
     value = $.cookie(key)

     # 删除
     $.cookie(key, null)
    */

    /*
    1、点击分类，选中对应分类 [解决: 记录下标]
    2、对应的分类商品显示  [解决: 参分类ID]
    3、当页面切换到其他页面后，再返回，下标和分类数据不匹配 [解决: 将点击下标传递给服务器， cookie]
    */


    // 你刚才点击了哪个？ 就是对应的样式添加上
    // var index = localStorage.getItem('index')
    var index = $.cookie('index');
    console.log(index);
    if (index){ // 有点击，有下标
        $('.type-slider li').eq(index).addClass('active')
    } else {
        $('.type-slider li:first').addClass('active')
    }


    // 侧边栏(分类) 点击
    // 问题: 点击显示效果是可以的，但因为a标签的原因，点击后添加的样式会因为 [重新加载页面]，导致样式又消失
    $('.type-slider li').click(function () {
        // $(this)  当前点击的对象
        // $(this).addClass('active')

        // 解决: 点击后，记录下标
        // localStorage.setItem('index', $(this).index())
        $.cookie('index', $(this).index(), {expires: 3, path: '/'})
    });
    
    
    // 子类
    var categoryShow = false;
    $('#category-bt').click(function () {
        // console.log(categoryShow)
        // if (categoryShow){  // 隐藏
        //     categoryShow = false
        //     $('.category-view').hide()
        // } else { // 显示
        //     categoryShow = true
        //     $('.category-view').show()
        // }

        // 取反
        categoryShow = !categoryShow;
        categoryShow ? categoryViewShow() : categoryViewHide()

        console.log('子类点击')
    });

    function categoryViewShow() {
        $('.category-view').show();
        $('#category-bt i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

        sortViewHide()
        sortShow = false
    }

    function categoryViewHide() {
        $('.category-view').hide()
        $('#category-bt i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    }
    
    // 排序
    var sortShow = false
    $('#sort-bt').click(function () {
        sortShow = !sortShow
        sortShow ? sortViewShow() : sortViewHide()

        console.log('排序点击')
    })

    function sortViewShow() {
        $('.sort-view').show()
        $('#sort-bt i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

        categoryViewHide()
        categoryShow = false
    }

    function sortViewHide() {
        $('.sort-view').hide()
        $('#sort-bt i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    }
    
    // 灰色蒙层
    $('.bounce-view').click(function () {
        sortViewHide()
        sortShow = false

        categoryViewHide()
        categoryShow = false
    })
})