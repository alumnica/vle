$(document).ready(function () {

    $('.block').each(function () {

        let theState = $(this).attr('state');
        $(this).addClass(theState);

        let attr = $(this).attr('data-n');

        // For some browsers, `attr` is undefined; for others,
        // `attr` is false.  Check for both.
        if (typeof attr !== typeof undefined && attr !== false) {

            //append to section if already has data-n
            let theBlocknum = $(this).attr('data-n');
            let theBlock = $('#' + theBlocknum);
            $(this).appendTo(theBlock);
        }
    });


});