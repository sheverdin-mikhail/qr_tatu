$(document).ready(function() {
    $('#mobileNav').change(function(){activeSettings(this.options[this.selectedIndex].getAttribute("data-select"));});
    const menu = document.querySelectorAll('.pc-nav-item');
    function pcNav(){
      menu.forEach((item) =>
      item.classList.remove('active'));
      this.classList.add("active");
      activeSettings($(this).attr("data-select"));
    }
    function activeSettings(e){
      let k = String(e);
      $('.controls-item').css('display','none');
      $("#"+k).css('display','block');
    }
    menu.forEach((item) =>
    item.addEventListener('click',pcNav));
    $('#enterForm').on('show.bs.modal', function(event){
      $('body .modal-box .modal-dialog').removeClass('modal-xl');
      $('#loginForm').css('display','block');
      $('#validAgeForm').css('display','none');
      $('#createUserForm').css('display','none');
    });   //.css('width','auto')
    $('#createUser').on('click', function(){
      $('body .modal-box .modal-dialog').addClass('modal-xl');
      $('#loginForm').css('display','none');
      $('#validAgeForm').css('display','block');
    });  //.animate({width: '100%'}, 600 )
    $('#confirmAge').on('click', function(){
      $('#validAgeForm').css('display','none');
      $('#createUserForm').css('display','block');
    });
    $('#resetStep').on('click', function(){
      $('body .modal-box .modal-dialog').removeClass('modal-xl');
      $('#loginForm').css('display','block');
      $('#validAgeForm').css('display','none');
      $('#createUserForm').css('display','none');
    });
});