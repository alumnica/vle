$(document).ready(function () {
    $('#moments').fullpage({
        verticalCentered: false,
        slidesNavigation: true,
        slidesNavPosition: 'bottom',
        loopHorizontal: false,


    });


    $('.end-uoda-btn').click(function () {

        let timeSpentOnPage = TimeMe.getTimeOnCurrentPageInSeconds();
        let duration = timeSpentOnPage.toString().slice(0, -1);
        duration = `PT${duration}S`;
        console.log(duration);


        $.ajax({
            method: 'POST',
            type: 'POST',
            url: '/api/microodas/' + learner + "," + microoda + "," + duration + "/",
            success: function (data) {
                window.location.href = "/odas/" + data.oda + "/";
        }

        }
        );
    });
});

