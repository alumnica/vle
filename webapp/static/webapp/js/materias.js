$(document).ready(function () {

    $('.block').each(function () {

        var theState = $(this).attr('state');
        $(this).addClass(theState);

        var attr = $(this).attr('data-n');

        // For some browsers, `attr` is undefined; for others,
        // `attr` is false.  Check for both.
        if (typeof attr !== typeof undefined && attr !== false) {

            //append to section if already has data-n
            var theBlocknum = $(this).attr('data-n');
            var theBlock = $('#' + theBlocknum);
            $(this).appendTo(theBlock);
        }
    });
});