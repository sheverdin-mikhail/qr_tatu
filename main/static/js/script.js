$(document).ready(function(){
    var dateMask = IMask(
      document.getElementById('Birthday'), {
        mask: Date,
        min: new Date(1990, 0, 1),
        max: new Date(),
        lazy: true,
      });
    $('#invalidCheck').on('click', function(){
        if($('#invalidCheck').is(':checked')){
            $('#confirmAge').prop('disabled', false)
        }else{
            $('#confirmAge').prop('disabled', true)
        }
    })
    $('#confirmAge').on('click', function(){
        var date_now = new Date();
        var input = dateMask.value.split('.')
        var input_date = new Date(input[2], input[1]-1, input[0])
        var age = Math.round((date_now - input_date)/ (365.25 * 24 * 60 * 60 * 1000))
        if(age>=18){
            $('#validAgeForm').css('display','none');
            $('#createUserForm').css('display','block');
        }else{
            $('body .modal-box .modal-dialog').removeClass('modal-xl');
            $('#loginForm').css('display','block');
            $('#validAgeForm').css('display','none');
            $('#createUserForm').css('display','none');
        }
          $('#validAgeForm').css('display','none');
        });

    $('#Rights').on('scroll', function(){

       var p_sh = $(this)[0].scrollHeight,
            p_h = $(this).height();

          if($(this).scrollTop() >= p_sh - p_h){
            $('#invalidCheck').prop('disabled', false)
          }else{
            $('#invalidCheck').prop('disabled', true)
          }
    });
})