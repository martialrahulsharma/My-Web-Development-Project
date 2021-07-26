$(function(){
    $('.password-show').click(function(event){
        $(this).toggleClass("fa-eye fa-eye-slash");
        var x = $(".input-control").attr("type");
        if(x == "password"){
            $('.input-control').attr("type","text");
        }else{
            $('.input-control').attr("type","password");
        }
    });
});

