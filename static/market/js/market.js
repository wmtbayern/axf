$(function () {
    /* 熟悉jquery.cookie 用法
     # 设置
     $.cookie(key, value, arg)
     # 获取
     value = $.cookie(key)
     # 删除,就是设置为空null
     $.cookie(key, null)
    */
    /*
    1、点击分类，选中对应分类 [解决: 记录下标]
    2、对应的分类商品显示  [解决: 参分类ID]
    3、当页面切换到其他页面后，再返回，下标和分类数据不匹配 [解决: 将点击下标传递给服务器， cookie]
    */

    // 你刚才点击了哪个？ 就是对应的样式添加上
    // var index = localStorage.getItem('index')
    //从cookie里面获取index
    var index = $.cookie('index')
    console.log(index);
    if (index){ // 有点击，有下标
        $('.type-slider li').eq(index).addClass('active')
    } else {  //没有点击就没有下标,默认显示第一个分类
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
    })
    
    
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
        categoryShow ? categoryViewShow() : categoryViewHide();

        console.log('子类点击')
    });

    function categoryViewShow() {
        $('.category-view').show();
        $('#category-bt i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

        sortViewHide();
        sortShow = false
    }

    function categoryViewHide() {
        $('.category-view').hide();
        $('#category-bt i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    }
    
    // 排序
    var sortShow = false;
    $('#sort-bt').click(function () {
        sortShow = !sortShow;
        sortShow ? sortViewShow() : sortViewHide();

        console.log('排序点击')
    });

    function sortViewShow() {
        $('.sort-view').show();
        $('#sort-bt i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

        categoryViewHide();
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

    ///////////////////////////////////////
    // 隐藏处理

    // $('.bt-wrapper>.glyphicon-minus').hide()
    // $('.bt-wrapper>i').hide()

    // 减号一开始是处于隐藏状态,有数量之后才显示
    $('.bt-wrapper .num').each(function () {
        var num = parseInt($(this).html())
        if (num){   // 有数值
            $(this).prev().show()
            $(this).show()
        } else {    // 没有数值
            $(this).prev().hide()
            $(this).hide()
        }
    })

    // console.log($('#main-content').prev().prev() )

    // 点击加操作

    $('.bt-wrapper >.glyphicon-plus').click(function () {
        // 需要传递 user、goods

        // user 因为状态保持，所以可以不用传递 [前提必须是先登录]

        // 哪件商品?  >>>  每个按钮身上有对应的属性
        request_data = {
            'goodsid': $(this).attr('data-goodsid')
        }

        // 保存 当前操作按钮对象
        var $that = $(this)
        //注意ajax的写法,第二个参数是客户端发送过去的数据
        // ,第三个是回调函数,处理服务器发送回来的数据 response_data{}

        $.get('/axf/addcart/', request_data, function (response) {
            console.log(response)

            if (response.status == -1){ // 未登录

                // 设置cookie
                $.cookie('back', 'market', {expires: 3, path: '/'})

                window.open('/axf/login/', '_self')
            } else  if (response.status ==1 ) {
                // 用户有登陆,可以操作加减操作
                // 下面这个写法是有问题，改变的是所有的带num的标签
                // $('.bt-wrapper .num').html(response.number)

                // 用兄弟节点 [操作按钮 this]
                // 在js 和jquery 里面 是谁调用 this就指向谁,当前标签
                // 当前函数是ajax触发的 ，所以 $(this) 指向 ajax回调函数,
                //在ajax 里面不能直接用this  指 代 当 前 标 签,
                // $(this).prev().html(response.number)
                //要用$that= $(this)来替代
                // 设置个数
                $that.prev().html(response.number)

                // 如果点击加号,就设置数字和减号标签都显示
                $that.prev().show()
                //前两个标签,就是减号,   只是兄弟标签之间可以使用prev()
                $that.prev().prev().show()
            }
        })
    })

    // 点击减操作
    //注意选中标签的写法    $('. > . ') 选中第一个标签 的 子标签
    $('.bt-wrapper>.glyphicon-minus').click(function () {
        //ajax请求都这样写$(this)

        var $that = $(this)
        request_data = {
            'goodsid': $(this).attr('data-goodsid')
        }

        $.get('/axf/subcart/', request_data, function (response) {
            console.log(response)

            if (response.status == 1){  //请求成功

                if (response.number) {
                    //html()  把参数写入到html标签里面
                    $that.next().html( response.number )
                } else {
                    $that.next().hide()
                    $that.hide()
                }
            }
        })
    })
})