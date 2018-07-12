$(document).ready(function () {
    $('#moments').fullpage({
        verticalCentered: false,
        slidesNavigation: true,
        slidesNavPosition: 'bottom',
        loopHorizontal: false,

 
    });

    $('.end-uoda-btn').click(function () {

        $.ajax({
            url: '/api/microodas/'+learner+","+microoda,


        });
    });
});