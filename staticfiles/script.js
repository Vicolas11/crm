$(function() {
    // $('.delete-btn').click(function(){
    //     $('.delete-model').css('display','block')
    // }) 
    $('.nav-tabs a:first').tab('show')
    $('.nav-tabs #profile-tab').tab('show')

    $(".navbarcus .dropdown .dropbtn").click(function(event){
        $(".navbarcus .dropdown .dropdown-content").css("display", "block");
    });

    $(window).hover(function(event){
        if (event.target == $(".navbarcus .dropdown .dropdown-content")) 
        {
            $(".navbarcus .dropdown .dropdown-content").css("display", "none");    
        }
    });
    
});