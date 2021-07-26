$(document).ready(function () {
    $('form').on('click', '#sentOtp', function (event) {
    
        $.ajax({
            data: {
                email : $('#username').val(),
            },
            type: 'POST',
            url: '/forgate_password/sent_otp',
            beforeSend: function () {
               $(".modal").show();
            },
            complete: function () {
                $(".modal").hide();
            }
    
        })
        .done(function(data){
            if(data.msg){
                $('#msg').text(data.msg).show();
                $('#otpdiv').css('display','show').show();
            }else{
                $('#msg').text(data.error).show();
            }
        });
        event.preventDefault();
    });

    $('form').on('click', '#VerifyOtpButton', function (event) {
        var otpVal = $('#otpfield').val();
        var otpCheck = $.isNumeric(otpVal);
        if (otpCheck) {  
            
            $.ajax({
                data: {
                    OTP : $('#otpfield').val(),
                },
                type: 'POST',
                url: '/forgate_password/validate_otp',
    
                beforeSend: function () {
                    $(".modal").show();
    
                 },
                 complete: function () {
                     $(".modal").hide();
    
                 }
            })
            .done(function(data){
                if(data.OTP){
                    alert('Verified OTP');
                    $('#pswdiv').css('display','show').show();
                }else{
                    alert(data.error);
                    $('#msg').text(data.error).show();
                }
            });
            event.preventDefault();

            } else {  
            alert('Check your input type must be Numeric');
            }
        
    });

    $('#newpsww').focusout(function(event){
        
        $.ajax({
            data: {
                psw : $('#newpsww').val(),
            },
            type: 'POST',
            url: '/password_validation',
            
    
        })
        .done(function(data){
            if(data.error){
                $('#pswerror').text("Invalid Password:- " + data.error).show();
                $('#pswerror').css('display','show');
                $('#pswmsg').hide();
            }else{
                $('#pswmsg').text(data.msg).show();
                $('#pswerror').hide();
            }
        });
        
        event.preventDefault();
    });

});
