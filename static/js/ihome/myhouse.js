$(document).ready(function(){
    $(".auth-warn").show();
})

$(document).ready(function(){
    $.get('/home/house_info/', function(data){
        if(data.code == '200'){
            $('.auth-warn').hide()
            $('#house-list').show()
            for(var i=0; i<data.house_info.length;i++){
                var house = '<li>'
                house +='<a href="/home/detail/?house_id='+ data.house_info[i].id+'">'
                house +='<div class="house-title">'
                house +='<h3>房屋ID:'+data.house_info[i].id + ' —— '+data.house_info[i].title +'</h3>'
                house +='</div><div class="house-content">'
                house +='<img alt="" src="/static/media/'+ data.house_info[i].image+'">'
                house +='<div class="house-text"><ul>'
                house +='<li>位于:'+data.house_info[i].area+'</li>'
                house +='<li>价格：￥'+ data.house_info[i].price+'/晚</li>'
                house +='<li>发布时间：' + data.house_info[i].create_time + '</li>'
                house +='</ul></div></div></a></li>'
                $('#houses-list').append(house)

            }

        }
        if(data.code == '10011'){
            $('.auth-warn').show()
            $('#house-list').hide()
        }

    })

})