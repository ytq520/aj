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
$.get('/order/lorder_info/', function(data){
    for(i in data.lorder_info){
        var lorder = '<li order-id="'+data.lorder_info[i].order_id+'">'
        lorder += '<div class="order-title">'
        lorder += '<h3>订单编号：'+data.lorder_info[i].order_id+'</h3>'
        lorder += '<div class="fr order-operate">'
        lorder += '<button type="button" class="btn btn-success order-accept" data-toggle="modal" data-target="#accept-modal">接单</button>'
        lorder += '<button type="button" class="btn btn-danger order-reject" data-toggle="modal" data-target="#reject-modal">拒单</button>'
        lorder += '</div>'
        lorder += '</div>'
        lorder += '<div class="order-content">'
        lorder += '<img src="/static/media/'+data.lorder_info[i].image+'">'
        lorder += '<div class="order-text">'
        lorder += '<h3>'+data.lorder_info[i].house_title+'</h3>'
        lorder += '<ul>'
        lorder += '<li>创建时间：'+data.lorder_info[i].create_date+'</li>'
        lorder += '<li>入住日期：'+data.lorder_info[i].begin_date+'</li>'
        lorder += '<li>离开日期：'+data.lorder_info[i].end_date+'</li>'
        lorder += '<li>合计金额：￥'+data.lorder_info[i].amount+'(共'+data.lorder_info[i].days+'晚)</li>'
        lorder += '<li>订单状态：'
        lorder += '<span>'+data.lorder_info[i].status+'</span></li>'
        lorder += '<li>客户评价：'+data.lorder_info[i].comment+'</li>'
        lorder += '</ul></div> </div></li>'
        $('.orders-list').append(lorder)
    }
})
$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-accept").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-accept").attr("order-id", orderId);
        $(".modal-accept").click(function(){
            $.ajax({
                url: '/order/accept/',
                type: 'POST',
                data: {'orderId':orderId},
                dataType: 'json',
                success: function(data){
                    if (data.code == '200'){
                        $('.order-accept').hide();
                        $('.order-reject').hide();
                        location.reload();
                    }
                },
                error: function(data){
                    alert('no');
                }
            })
        })
    });
    $(".order-reject").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id")
        $(".modal-reject").attr("order-id", orderId)
        $(".modal-reject").click(function(){
            $.ajax({
                url: '/order/my_comment/',
                type: 'POST',
                data: {'orderId':orderId, 'reason': $('#reject-reason').val()},
                dataType: 'json',
                success: function(data){
                    if (data.code == '200'){
                        $('.order-accept').hide();
                        $('.order-reject').hide();
                        location.reload();
                    }
                },
                error: function(data){
                    alert('no');
                }
            })
        })
    });

});