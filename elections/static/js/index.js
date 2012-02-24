$(document).ready(function(){
        $('#carou').carousel();
    $('#carou').mouseenter(function() {
        $(this).carousel('pause');
    }).mouseleave(function() {
        $(this).carousel('next');
    }); 
      

        
});
