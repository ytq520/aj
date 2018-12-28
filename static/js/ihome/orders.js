//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
$.get('/order/my_order/', function(data){
    for(i in data.order_info){
        var order = '<li order-id="'+data.order_info[i].order_id+'">'
        order += '<div class="order-title">'
        order += '<h3>订单编号：'+ data.order_info[i].order_id +'</h3>'
        order +='<div class="fr order-operate">'
        order +='<button type="button" class="btn btn-success order-comment" data-toggle="modal" data-target="#comment-modal">发表评价</button>'
        order +='</div>'
        order +='</div>'
        order +='<div class="order-content">'
        order +='<img src="/static/media/'+data.order_info[i].image+'">'
        order +=' <div class="order-text">'
        order +='<h3>订单</h3>'
        order +='<ul>'
        order +='<li>创建时间：'+data.order_info[i].create_date+'</li>'
        order +='<li>入住日期：'+data.order_info[i].begin_date+'</li>'
        order +='<li>离开日期：'+data.order_info[i].end_date+'</li>'
        order +='<li>合计金额：'+data.order_info[i].amount+'元(共'+data.order_info[i].days+'晚)</li>'
        order +='<li>订单状态：'
        order +='<span>'+data.order_info[i].status+'</span>'
        order +='</li>'
        order +='<li>我的评价：'+ data.order_info[i].comment +'</li>'
        order +='<li>拒单原因：</li>'
        order += '</ul></div></div></li>'
        $('.orders-list').append(order)

    }
    $(".order-comment").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-comment").attr("order-id", orderId);
        $('.modal-comment').click(function(){
            $.ajax({
                url: '/order/my_comment/',
                type: 'POST',
                data: {'orderId':orderId, 'comment': $('#comment').val()},
                dataType: 'json',
                success: function(data){
                    if (data.code == '200'){
                        $('.order-operate').hide()
                        location.assign()

                    }
                },
                error: function(data){
                    alert('no');
                }
            })


        })
    });
})

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);

});

