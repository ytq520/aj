function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


$('#form-auth').submit(function(e){
    e.preventDefault()
    var real_name = $('#real-name').val();
    var id_card = $('#id-card').val();
    $.ajax({
        url:'/user/auth/',
        data:{'real_name': real_name, 'id_card':id_card},
        type:'POST',
        dataType:'json',
        success: function(data){
            if(data.code == '10009' | data.code == '10010' | data.code == '10007' | data.code == '10007'){
                $('.error-msg').html(data.msg)
                $('.error-msg').show()
            }
            if(data.code == '200'){
                $('.btn-success').hide()
                $('#id-card').attr('disabled', disabled)
            }

        },
        error: function(data){
            alert('no')
        }
    })
})
