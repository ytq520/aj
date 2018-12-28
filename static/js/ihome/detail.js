function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    })
    $(".book-house").show();
})

$(document).ready(function(){
    $('.book-house').show();
    var search_url = location.search
    // http//127.0.0.1:8000/house/detail/?house_id=id
    // search_url: ?house_id=id
    house_id = search_url.split('=')[1]
    // spilt() 分割
    $.get('/home/detail/'+ house_id + '/', function(data){
        console.log(data)
        if(data.code == '200'){
            for(i in data.house.images){
                var swiper_li = '<li class="swiper-slide "><img src="/static/media/'+ data.house.images[i] +'"></li>'
                $('.swiper-wrapper').append(swiper_li)
            }
            var mySwiper = new Swiper('.swiper-container',{
                loop:true,
                autoplay: 2000,
                autoplayDisableOnInteraction:false,
                pagination:'.swiper-pagination',
                paginationType: 'fraction'
            })
            $('.house-price').html('￥<span>'+ data.house.price +'</span>/晚')
            $('.house-title').html(data.house.title)
            $('.landlord-pic').html('<img src="/static/media/'+ data.house.user_avatar +'">')
            $('.landlord-name').html('房东： <span>'+ data.house.user_name +'</span>')
            $('.text-center').html('<li>地址内容'+ data.house.address +'</li>')
            $('#icon-house').html('<h3>出租'+data.house.room_count +'间</h3>'+'<p>房屋面积:'+data.house.acreage +'平米</p>'+' <p>房屋户型:'+ data.house.unit +'</p>')
            $('#icon-user').html('<h3>宜住'+ data.house.capacity +'人</h3></div>')
            $('#icon-bed').html('<h3>卧床配置</h3>'+'<p>'+ data.house.beds +'</p></div>')
            $('.house-info-list').html('<li>收取押金<span>'+data.house.deposit+'</span></li>'+'<li>最少入住天数<span>'+ data.house.min_days +'</span></li>'+'<li>最多入住天数<span>'+ data.house.max_days +'</span></li>')
            var house_facility_list = ''
            for(var i=0; i<data.facility.length;i++){
                console.log(data.facility[i].css, data.facility[i].name)
                house_facility_list +='<li>'+'<span class="'+ data.facility[i].css +'"></span>'+ data.facility[i].name +'</li>'
            }
            $('.clearfix').html(house_facility_list)
            $('.book-house').attr('href','/order/booking/?house_id='+ house_id +'')
            // 判断是否显示预定按钮
            if(data.booking==1){
                $('.book-house').show()
            }else{
                $('.book-house').hide()
            }
        }
    })

})