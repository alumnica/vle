$(document).ready(function () {
    $('#moments').fullpage({
        verticalCentered: false,
        slidesNavigation: true,
        slidesNavPosition: 'bottom',
        loopHorizontal: false,

 
    });

    $('#end_btn').click(function () {

        $.ajax({
            url: '/api/microodas/'+learner+","+microoda,
            success: function(data){
                swal('success');
            }

        });
    });
});