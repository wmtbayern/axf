$(function () {
    $('.register').width(innerWidth);

   $('#email input').blur(function () {

        var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$"); //正则表达式

        // 空，不需要验证处理
        if ($(this).val() == '') return

        // 格式是否正确
        if (reg.test( $(this).val() ) ){  // 符合
            // 账号是否可用 [必须发给服务器]
            // 只需要 服务器 提示 可用true/不可用false
            // 通过ajax和服务器通信

            request_data = {
                'email': $(this).val()};

            $.get('/axf/checkemail/', request_data, function (response) {   // 回调函数
                // 客户端接受到数据之后的处理
                if (response.status){   // 1可用
                    //attr()是用于给元素设置指定的属性或返回指定属性的值
                    $('#email-t').attr('data-content', '账号可用').popover('hide')

                    $('#email').removeClass('has-error').addClass('has-success')
                    $('#email input').removeClass('glyphicon-remove').addClass('glyphicon-ok')
                } else {    // 0不可用
                    $('#email-t').attr('data-content', response.msg).popover('show')

                    $('#email').removeClass('has-success').addClass('has-error')
                    $('#email input').removeClass('glyphicon-ok').addClass('glyphicon-remove')
                }
            })

        } else {    // 不符合
            $('#email-t').attr('data-content', '格式不正确').popover('show')

            $('#email').removeClass('has-success').addClass('has-error')
            $('#email>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })


    //拿到输入框里的数据,再处理
    //邮箱验证   失去焦点,就是输入完成,这时可以给出提示
























})
