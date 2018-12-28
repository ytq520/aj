function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$.ajax({
    url:'/home/my_area/',
    type: 'GET',
    dateType: 'json',
    success: function(data){
        for(i in data.area){
            s='<option value="'+data.area[i].id+'">'+ data.area[i].name +'</option>'
            $('#area-id').append(s)
        };
        for(n in data.facility){
            k='<li>'+ '<div class="checkbox">' + '<label>'+ '<input type="checkbox" name="facility" value="'+data.facility[n].id+'">' + data.facility[n].name + '</label>' + '</div>' + '</li>'
            $('.clearfix').append(k)
        }
    },
    error:function(data){
        alert('失败')
    }
})



$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $('#form-house-info').submit(function(e){
        e.preventDefault();
        //        var house_title = $('#house-title').val();
        //        var house_price = $('#house-price').val();
        //        var area_id = $('#area-id').val();
        //        var address = $('#address').val();
        //
        //        var room_count = $('#room_count').val();
        //        var unit = $('#unit').val();
        //        var capacity = $('#capacity').val();
        //        var beds = $('#beds').val();
        //        var deposit = $('#deposit').val();
        //        var min_days = $('#min_days').val();
        //        var max_days = $('#max_days').val();
        //
        //        var facility = $('#facility').val();

        //  $(this).ajaxSubmit 直接获取整个 表单数据
        $(this).ajaxSubmit({
            url: '/home/newhouse/',
            type: 'POST',
            dataType: 'json',
            success: function(data){
                alert('yes');
                $('#house-id').val(data.house_id);
                $('#form-house-info').attr('style', 'display:none');
                $('#form-house-image').attr('style', 'display:block');

            },
            error: function(data){
                alert('no');
            }
        })
    });


    $('#form-house-image').submit(function(e){
        e.preventDefault();

        $(this).ajaxSubmit({
            url: '/home/house_img/',
            type: 'POST',
            dataType: 'json',
            success: function(data){
                //alert('yes info');
                if (data.code == 200){
                    //alert('200')
                    console.log(i)
                    $('#form-house-image').prepend('<img src="' + '/static/media/' + data.img +'">');
                }
            },
            error: function(data){
                alert('no');
            }
        })
    });
})

