$(document).ready(function () {
    $('.block').on('click', function (e) {
        e.stopPropagation(); // <--------------stop here
        $('.thetip').fadeOut(200);
        $('.thetip', this).fadeToggle('150');
    });
    $(document).click(function () { // you don't need the else part to fadeout
        let $el = $(".thetip");
        if ($el.is(":visible")) {
            $el.fadeOut(200);
        }
    });
});