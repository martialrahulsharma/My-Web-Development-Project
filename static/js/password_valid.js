$(document).ready(function () {
    // $('form').on('click', '#password', function (event) {
        $('#pasw').focusout(function(event){

            $.ajax({
                data: {
                    psw : $('#pasw').val(),
                },
                type: 'POST',
                url: '/password_validation',
                
        
            })
            .done(function(data){
                if(data.error){
                    alert("Invalid Password: " + data.error);
                    // $('#pswerror').text("Invalid Password:- " + data.error).show();
                    // $('#pswerror').css('display','show');
                    // $('#pswmsg').hide();
                }else{
                    alert(data.msg);
                    // $('#pswmsg').text(data.msg).show();
                    // $('#pswerror').hide();
                }
            });
            
            event.preventDefault();
        });
        
        
    });

    $(function(){
  
        $('#eye').click(function(){
             
              if($(this).hasClass('fa-eye-slash')){
                 
                $(this).removeClass('fa-eye-slash');
                
                $(this).addClass('fa-eye');
                
                $('#password').attr('type','text');
                  
              }else{
               
                $(this).removeClass('fa-eye');
                
                $(this).addClass('fa-eye-slash');  
                
                $('#password').attr('type','password');
              }
          });
      });
