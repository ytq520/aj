function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
})


$(document).ready(function(){
    var house_id = location.search.split('=')[1]
    $.get('/home/detail/'+ house_id +'/',function(data){
        var booking = '<img src="/static/media/'+data.house.images[0]+'">'
        booking += '<div class="house-text">'
        booking += '<h3>'+data.house.title+'</h3>'
        booking += '<p>￥<span>'+ data.house.price +'</span>/晚</p>'
        booking += '</div>'
        $('.house-info').html(booking)
    })
    $('.submit-btn').click(function(){
        var start_data = $('#start-date').val()
        var end_data = $('#end-date').val()
        $.ajax({
            url:'/order/my_booking/',
            data:{'start_data':start_data, 'end_data':end_data, 'house_id':house_id},
            dataType:'json',
            type:'POST',
            success:function(data){
                if(data.code == '200'){
                    location.href = '/order/orders/'
                }
            },
            error:function(data){
                console.log('失败')
            }
        })
    })
})