$(document).ready(function () {
    $('#moments').fullpage({
        verticalCentered: false,
        slidesNavigation: true,
        slidesNavPosition: 'bottom',
        loopHorizontal: false,


    });


    $('.end-uoda-btn').click(function () {

        var timeSpentOnPage = TimeMe.getTimeOnCurrentPageInSeconds();
        var duration = timeSpentOnPage.toString().slice(0, -1);
        duration = `P${duration}S`;
        console.log(duration);



        $.ajax({
            url: '/api/microodas/' + learner + "," + microoda + "," + duration,



        });
    });
});

