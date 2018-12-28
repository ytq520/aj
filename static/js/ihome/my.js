function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){


})

$.ajax({
    url:'/user/my_get/',
    type: 'GET',
    dataType:'json',
    success: function(data){
        i_src='/static/media/'+ data.img;
        if(data.code == '200'){
            $('#user-name').text(data.name);
            $('#user-mobile').text(data.phone);
            $('#user-avatar').attr("src", i_src);
        }
    },
    error: function(data){
        alert('失败')
    }

})